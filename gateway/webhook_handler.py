"""
MediaAgentIQ — Webhook Handler

FastAPI routes that receive events from Slack and Teams,
route them to the correct agent, and return interactive responses.

Slack endpoints:
  POST /slack/events    — Events API (app_mention, message)
  POST /slack/commands  — Slash commands (/miq-*)
  POST /slack/actions   — Interactive component callbacks (button clicks)

Teams endpoints:
  POST /teams/messages  — Bot Framework Activity handler

Mount this router into app.py:
  from gateway.webhook_handler import gateway_router
  app.include_router(gateway_router, prefix="")
"""

import hashlib
import hmac
import json
import logging
import re
import time
from typing import Any, Dict, Optional

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from gateway.router import route, HELP_TEXT
from gateway.formatter import (
    format_slack,
    format_slack_error,
    format_slack_thinking,
    format_slack_unrecognized,
    format_teams,
    format_hope_created,
    format_hope_cancelled,
    format_hope_list,
)
from gateway.conversation import conversation_manager

logger = logging.getLogger("gateway.webhook")
gateway_router = APIRouter(tags=["Gateway — Channel Webhooks"])


# ─── Slack signature verification ─────────────────────────────────────────────

def _verify_slack_signature(
    body: bytes,
    timestamp: str,
    signature: str,
    signing_secret: str,
) -> bool:
    """Verify Slack request authenticity using HMAC-SHA256."""
    if abs(time.time() - float(timestamp)) > 300:
        return False   # Replay attack guard (5-min window)
    base = f"v0:{timestamp}:{body.decode()}"
    expected = "v0=" + hmac.new(
        signing_secret.encode(), base.encode(), hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


# ─── Core agent dispatch ───────────────────────────────────────────────────────

async def _dispatch_to_agent(
    platform: str,
    channel_id: str,
    user_id: str,
    text: str,
    respond_fn,             # async fn(payload: Dict) → None
) -> None:
    """
    Core dispatch logic shared by Slack events, slash commands, and Teams messages.

    1. Get/create conversation session
    2. Route text → intent
    3. Run agent
    4. Format result
    5. Send interactive response back to channel
    """
    session = conversation_manager.get_or_create(platform, channel_id, user_id)
    history = session.get_history_for_llm()

    # Route
    intent = await route(text, conversation_history=history)
    session.add_user_turn(text, agent_key=intent.agent_key, params=intent.params)

    # System commands
    if intent.is_system_command:
        payload = await _handle_system_command(intent.system_command, platform, intent=intent)
        await respond_fn(payload)
        return

    # Unrecognized
    if not intent.agent_key or intent.confidence < 0.3:
        await respond_fn(format_slack_unrecognized(text))
        return

    # Send "thinking" placeholder immediately
    await respond_fn(format_slack_thinking(intent.agent_key))

    # Run agent
    try:
        from agents import AGENTS
        agent_cls = AGENTS.get(intent.agent_key)
        if not agent_cls:
            await respond_fn(format_slack_error(f"Agent '{intent.agent_key}' not found.", intent.agent_key))
            return

        agent = agent_cls()
        resolved_params = session.resolve_params(intent.params)
        result = await agent.process(resolved_params or text)

        session.add_agent_turn(intent.agent_key, result)

        # Format for channel
        if platform == "slack":
            payload = format_slack(intent.agent_key, result)
        else:
            payload = format_teams(intent.agent_key, result)

        await respond_fn(payload)

    except Exception as e:
        logger.error(f"Agent dispatch error [{intent.agent_key}]: {e}", exc_info=True)
        await respond_fn(format_slack_error(str(e), intent.agent_key))


async def _handle_system_command(command: str, platform: str, intent=None) -> Dict:
    """Handle status / connectors / help / HOPE system commands."""
    if command == "help":
        return {"blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": HELP_TEXT}}]}

    if command == "status":
        try:
            from agents import AGENTS
            agents_status = {k: {"ready": True, "mode": "demo"} for k in AGENTS}
            return format_slack("__status__", {"agents": agents_status}, system_command="status")
        except Exception as e:
            return format_slack_error(str(e))

    if command == "connectors":
        try:
            from connectors.registry import connector_registry
            dashboard = connector_registry.get_dashboard()
            return format_slack("__connectors__", dashboard, system_command="connectors")
        except Exception as e:
            return format_slack_error(str(e))

    # ── HOPE intents ──────────────────────────────────────────────────────────

    if command == "__hope_create__":
        return await _handle_hope_create(intent)

    if command == "__hope_cancel__":
        return await _handle_hope_cancel(intent)

    if command == "__hope_list__":
        return await _handle_hope_list(intent)

    return format_slack_unrecognized(command)


async def _handle_hope_create(intent) -> Dict:
    """Parse natural-language HOPE create command and register the rule."""
    try:
        raw_text = (intent.params or {}).get("raw_text", "")
        agent_key = intent.agent_key

        # Extract schedule keyword
        schedule = "IMMEDIATE"
        if re.search(r"\bevery (morning|day|daily)\b", raw_text, re.I):
            schedule = "DAILY 08:00 IST"
        elif re.search(r"\bevery week\b|\bweekly\b", raw_text, re.I):
            schedule = "WEEKLY MON 08:00 IST"

        # Extract priority
        priority = "NORMAL"
        if re.search(r"\bbreaking\b|\bcritical\b|\burgent\b", raw_text, re.I):
            priority = "CRITICAL"
        elif re.search(r"\bimmediately\b|\bright away\b|\basap\b", raw_text, re.I):
            priority = "HIGH"

        # Use the whole raw_text as condition; action defaults to Slack DM
        condition = raw_text
        action = f"Send Slack DM to user with summary"

        if agent_key:
            from agents import AGENTS
            agent_cls = AGENTS.get(agent_key)
            if agent_cls:
                agent = agent_cls()
                result = agent.add_hope_rule(condition, schedule, action, priority)
                return format_hope_created(result)

        # No specific agent — apply to all registered agents
        return format_hope_created({
            "rule_id": "hope_pending",
            "agent": agent_key or "all",
            "status": "created",
            "note": "No specific agent detected — specify an agent (e.g. 'archive agent') to register the rule.",
        })
    except Exception as e:
        logger.error(f"HOPE create error: {e}", exc_info=True)
        return format_slack_error(str(e))


async def _handle_hope_cancel(intent) -> Dict:
    """Cancel a HOPE rule by extracting the rule_id from the message."""
    try:
        raw_text = (intent.params or {}).get("raw_text", "")
        # Extract rule_id like hope_001
        m = re.search(r"\bhope_\d+\b", raw_text, re.I)
        rule_id = m.group(0).lower() if m else None

        if not rule_id:
            return format_slack_error("Could not find a rule ID (e.g. hope_001) in your message.")

        agent_key = intent.agent_key
        if agent_key:
            from agents import AGENTS
            agent_cls = AGENTS.get(agent_key)
            if agent_cls:
                agent = agent_cls()
                result = agent.cancel_hope_rule(rule_id)
                return format_hope_cancelled(result.get("rule_id", rule_id))

        return format_hope_cancelled(rule_id)
    except Exception as e:
        logger.error(f"HOPE cancel error: {e}", exc_info=True)
        return format_slack_error(str(e))


async def _handle_hope_list(intent) -> Dict:
    """List all HOPE rules for the specified (or first available) agent."""
    try:
        import re as _re
        agent_key = intent.agent_key
        rules: list = []

        if agent_key:
            from agents import AGENTS
            agent_cls = AGENTS.get(agent_key)
            if agent_cls:
                agent = agent_cls()
                rules = agent.list_hope_rules()

        return format_hope_list(rules, agent_key=agent_key or "all")
    except Exception as e:
        logger.error(f"HOPE list error: {e}", exc_info=True)
        return format_slack_error(str(e))


# ─── Slack: Events API ─────────────────────────────────────────────────────────

@gateway_router.post("/slack/events")
async def slack_events(
    request: Request,
    background_tasks: BackgroundTasks,
    x_slack_request_timestamp: Optional[str] = Header(None),
    x_slack_signature: Optional[str] = Header(None),
):
    """
    Receives Slack Events API payloads.
    Handles: url_verification challenge, app_mention, message events.
    """
    body = await request.body()
    payload = json.loads(body)

    # Slack URL verification handshake
    if payload.get("type") == "url_verification":
        return JSONResponse({"challenge": payload["challenge"]})

    # Signature verification (skip if signing secret not configured)
    try:
        from settings import settings
        if settings.SLACK_SIGNING_SECRET and x_slack_signature:
            if not _verify_slack_signature(
                body, x_slack_request_timestamp,
                x_slack_signature, settings.SLACK_SIGNING_SECRET
            ):
                raise HTTPException(status_code=403, detail="Invalid Slack signature")
    except ImportError:
        pass

    event = payload.get("event", {})
    event_type = event.get("type")

    if event_type in ("app_mention", "message") and not event.get("bot_id"):
        text = event.get("text", "")
        # Strip bot mention prefix: <@BOTID> some text
        text = " ".join(w for w in text.split() if not w.startswith("<@"))
        channel = event.get("channel", "")
        user = event.get("user", "unknown")

        # Import Slack client lazily
        async def respond(msg_payload: Dict):
            try:
                from connectors.channels.slack import slack_channel
                await slack_channel.send_message(channel, msg_payload)
            except Exception as e:
                logger.error(f"Slack send error: {e}")

        background_tasks.add_task(
            _dispatch_to_agent, "slack", channel, user, text, respond
        )

    # Slack expects 200 immediately
    return Response(status_code=200)


# ─── Slack: Slash commands ─────────────────────────────────────────────────────

@gateway_router.post("/slack/commands")
async def slack_slash_command(
    request: Request,
    background_tasks: BackgroundTasks,
):
    """
    Receives Slack slash command payloads (application/x-www-form-urlencoded).
    Immediately returns HTTP 200 with 'Processing...' text (Slack 3s limit),
    then dispatches agent in background.
    """
    form = await request.form()
    command = form.get("command", "")
    text = form.get("text", "")
    channel_id = form.get("channel_id", "")
    user_id = form.get("user_id", "unknown")
    response_url = form.get("response_url", "")

    full_text = f"{command} {text}".strip()

    async def respond_via_url(msg_payload: Dict):
        """Post response back to Slack via response_url (handles delayed responses)."""
        import httpx
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    response_url,
                    json={**msg_payload, "response_type": "in_channel"},
                    timeout=10,
                )
        except Exception as e:
            logger.error(f"Slack response_url error: {e}")

    background_tasks.add_task(
        _dispatch_to_agent, "slack", channel_id, user_id, full_text, respond_via_url
    )

    # Immediate Slack-compliant response
    return JSONResponse({
        "response_type": "ephemeral",
        "text": f"_Running {command}..._  ⏳",
    })


# ─── Slack: Interactive actions (button clicks) ────────────────────────────────

@gateway_router.post("/slack/actions")
async def slack_actions(
    request: Request,
    background_tasks: BackgroundTasks,
):
    """
    Handles Slack Block Kit interactive component callbacks.
    Called when a user clicks a button in an agent result card.
    """
    form = await request.form()
    payload = json.loads(form.get("payload", "{}"))

    actions = payload.get("actions", [])
    user = payload.get("user", {})
    channel = payload.get("channel", {})
    response_url = payload.get("response_url", "")
    user_id = user.get("id", "unknown")
    channel_id = channel.get("id", "")

    for action in actions:
        action_id = action.get("action_id", "")
        logger.info(f"Slack action: {action_id} from {user_id}")

        # Parse action_id: miq_<verb>_<agent>
        parts = action_id.split("_", 2)
        if len(parts) >= 3 and parts[0] == "miq":
            verb = parts[1]
            agent_key = parts[2]
            background_tasks.add_task(
                _handle_interactive_action, verb, agent_key,
                user_id, channel_id, response_url, payload
            )

    return Response(status_code=200)


async def _handle_interactive_action(
    verb: str,
    agent_key: str,
    user_id: str,
    channel_id: str,
    response_url: str,
    full_payload: Dict,
) -> None:
    """Process button click actions asynchronously."""
    import httpx

    action_map = {
        "export":       f"Exporting {agent_key} report...",
        "approve":      f"Approving {agent_key} decision...",
        "reject":       f"Rejecting {agent_key} decision...",
        "publish":      f"Publishing via {agent_key}...",
        "alert":        f"Sending alert from {agent_key}...",
        "hold":         "Holding content from broadcast...",
        "release":      "Releasing content for broadcast...",
        "sync":         "Syncing...",
        "override":     "Override applied.",
        "block":        "Blocking ad insertion...",
        "download":     "Preparing download...",
        "push":         "Pushing to automation server...",
        "copy":         "Copied to clipboard.",
    }

    message = action_map.get(verb, f"Processing action: {verb} on {agent_key}...")

    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                response_url,
                json={"text": f"✅ {message}", "replace_original": False},
                timeout=10,
            )
        except Exception as e:
            logger.error(f"Action response error: {e}")


# ─── Teams: Bot Framework ──────────────────────────────────────────────────────

@gateway_router.post("/teams/messages")
async def teams_messages(
    request: Request,
    background_tasks: BackgroundTasks,
):
    """
    Receives Microsoft Teams Bot Framework Activity payloads.
    Handles message activities and dispatches to agents.
    """
    body = await request.json()
    activity_type = body.get("type", "")

    if activity_type != "message":
        return JSONResponse({"type": "ok"})

    text = body.get("text", "").strip()
    # Remove @mention if present
    from_info = body.get("from", {})
    user_id = from_info.get("id", "unknown")
    conversation = body.get("conversation", {})
    channel_id = conversation.get("id", "teams-default")
    service_url = body.get("serviceUrl", "")
    activity_id = body.get("id", "")

    async def respond_teams(msg_payload: Dict):
        try:
            from connectors.channels.teams import teams_channel
            await teams_channel.send_activity(
                service_url=service_url,
                conversation_id=channel_id,
                activity_id=activity_id,
                payload=msg_payload,
            )
        except Exception as e:
            logger.error(f"Teams send error: {e}")

    background_tasks.add_task(
        _dispatch_to_agent, "teams", channel_id, user_id, text, respond_teams
    )

    return JSONResponse({"type": "ok"})


# ─── Health check ──────────────────────────────────────────────────────────────

@gateway_router.get("/gateway/health")
async def gateway_health():
    """Gateway health check."""
    return {
        "status": "ok",
        "active_sessions": conversation_manager.active_session_count,
        "endpoints": {
            "slack_events":   "/slack/events",
            "slack_commands": "/slack/commands",
            "slack_actions":  "/slack/actions",
            "teams_messages": "/teams/messages",
        }
    }
