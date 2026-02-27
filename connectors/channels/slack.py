"""
MediaAgentIQ — Slack Channel Connector

Bidirectional Slack integration:
  INBOUND  — receives user messages, slash commands, button clicks
             (handled by gateway/webhook_handler.py FastAPI routes)
  OUTBOUND — sends agent results as interactive Block Kit cards,
             sends proactive alerts from autonomous agents

Production requires:
  SLACK_BOT_TOKEN     — xoxb-... (Bot User OAuth Token)
  SLACK_SIGNING_SECRET — for webhook signature verification
  SLACK_DEFAULT_CHANNEL — default channel for proactive alerts

Demo mode:
  All send operations log to console instead of hitting the Slack API.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from connectors.base_connector import (
    BaseConnector,
    ConnectorCategory,
    ConnectorConfig,
    ConnectorStatus,
    HealthCheckResult,
    ToolDefinition,
    AuthType,
)

logger = logging.getLogger("connector.slack")


class SlackChannelConnector(BaseConnector):
    """
    Slack Bot connector for sending agent results as interactive cards.

    Agents call this connector to:
    - Send proactive alerts  (compliance violation, deepfake hold, trending spike)
    - Update existing messages (replace 'thinking...' with final result)
    - Post to specific channels  (#noc-alerts, #newsroom, #brand-safety)
    """

    def __init__(self, demo_mode: bool = True):
        from settings import settings as _settings
        super().__init__(ConnectorConfig(
            connector_id="slack",
            name="Slack",
            category=ConnectorCategory.COMMS,
            auth_type=AuthType.TOKEN,
            demo_mode=demo_mode,
            config={
                "bot_token":       getattr(_settings, "SLACK_BOT_TOKEN", ""),
                "signing_secret":  getattr(_settings, "SLACK_SIGNING_SECRET", ""),
                "default_channel": getattr(_settings, "SLACK_DEFAULT_CHANNEL", "#mediaagentiq"),
            }
        ))
        self._client = None

    # ── Connection ────────────────────────────────────────────────────

    async def authenticate(self) -> bool:
        if self.demo_mode:
            logger.info("Slack connector: DEMO mode — no real API calls")
            return True
        try:
            from slack_sdk.web.async_client import AsyncWebClient
            self._client = AsyncWebClient(token=self.config.config["bot_token"])
            response = await self._client.auth_test()
            logger.info(f"Slack authenticated as bot: {response.get('bot_id')}")
            return True
        except Exception as e:
            logger.error(f"Slack auth failed: {e}")
            return False

    async def health_check(self) -> HealthCheckResult:
        import time
        start = time.time()
        if self.demo_mode:
            self.last_health_check = HealthCheckResult(
                connector_id=self.connector_id,
                status=ConnectorStatus.CONNECTED,
                latency_ms=1.0,
                message="Demo mode — always healthy",
            )
            return self.last_health_check
        try:
            await self._client.auth_test()
            latency = (time.time() - start) * 1000
            self.last_health_check = HealthCheckResult(
                connector_id=self.connector_id,
                status=ConnectorStatus.CONNECTED,
                latency_ms=round(latency, 1),
                message="Slack API reachable",
            )
        except Exception as e:
            self.last_health_check = HealthCheckResult(
                connector_id=self.connector_id,
                status=ConnectorStatus.ERROR,
                message=str(e),
            )
        return self.last_health_check

    # ── Core operations ───────────────────────────────────────────────

    async def read(self, params: Dict[str, Any]) -> Any:
        """Read channel history or user info."""
        if self.demo_mode:
            return self._demo_response({
                "messages": [
                    {"user": "U123", "text": "Demo message 1", "ts": "1709000001.000001"},
                    {"user": "U456", "text": "Demo message 2", "ts": "1709000002.000002"},
                ]
            })
        channel = params.get("channel", self.config.config["default_channel"])
        limit = params.get("limit", 10)
        response = await self._client.conversations_history(channel=channel, limit=limit)
        return self._production_response({"messages": response.get("messages", [])})

    async def write(self, data: Any, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Send a message to a Slack channel.

        data: Dict with one of:
          - "blocks": [...] (Block Kit)
          - "text": "plain message"
          - "attachments": [...]

        params: {"channel": "#channel", "thread_ts": "...", "update_ts": "..."}
        """
        params = params or {}
        channel = params.get("channel") or data.get("channel") or self.config.config["default_channel"]

        if self.demo_mode:
            logger.info(f"[DEMO] Slack → {channel}: {str(data)[:120]}")
            return self._demo_response({"ts": f"demo.{datetime.now().timestamp()}", "channel": channel})

        try:
            kwargs = {"channel": channel}
            if "blocks" in data:
                kwargs["blocks"] = data["blocks"]
                kwargs["text"] = data.get("text", "MediaAgentIQ result")
            elif "text" in data:
                kwargs["text"] = data["text"]
            if "thread_ts" in params:
                kwargs["thread_ts"] = params["thread_ts"]

            # Update existing message vs new post
            if "update_ts" in params:
                kwargs["ts"] = params["update_ts"]
                response = await self._client.chat_update(**kwargs)
            else:
                response = await self._client.chat_postMessage(**kwargs)

            return self._production_response({
                "ts": response.get("ts"),
                "channel": response.get("channel"),
            })
        except Exception as e:
            logger.error(f"Slack write error: {e}")
            return self._error_response(str(e))

    # ── High-level helpers for agents ────────────────────────────────

    async def send_message(self, channel: str, payload: Dict) -> Dict:
        """Send a Block Kit payload to a channel."""
        return await self.write(payload, {"channel": channel})

    async def send_alert(
        self,
        title: str,
        message: str,
        severity: str = "warning",
        channel: str = None,
        agent: str = "",
    ) -> Dict:
        """
        Send a proactive alert from an autonomous agent.
        Used by: ComplianceAgent, DeepfakeAgent, SignalQualityAgent, etc.
        """
        emoji_map = {"critical": "🚨", "warning": "⚠️", "info": "ℹ️", "ok": "✅"}
        emoji = emoji_map.get(severity, "🔔")
        blocks = [
            {"type": "section", "text": {"type": "mrkdwn",
             "text": f"{emoji} *{title}*\n{message}"}},
            {"type": "context", "elements": [
                {"type": "mrkdwn", "text": f"MediaAgentIQ {agent} • {datetime.now().strftime('%H:%M:%S')}"}
            ]},
        ]
        return await self.write(
            {"blocks": blocks},
            {"channel": channel or self.config.config["default_channel"]}
        )

    async def update_message(self, channel: str, ts: str, payload: Dict) -> Dict:
        """Replace the 'thinking...' placeholder with the actual result."""
        return await self.write(payload, {"channel": channel, "update_ts": ts})

    # ── MCP Tool Definitions ──────────────────────────────────────────

    def get_tool_definitions(self) -> List[ToolDefinition]:
        return [
            ToolDefinition(
                name="slack_send_message",
                description="Send a message or Block Kit card to a Slack channel",
                input_schema={
                    "type": "object",
                    "properties": {
                        "channel":  {"type": "string", "description": "Channel name or ID"},
                        "text":     {"type": "string", "description": "Plain text fallback"},
                        "blocks":   {"type": "array",  "description": "Slack Block Kit blocks"},
                    },
                    "required": ["channel"],
                },
                connector_id=self.connector_id,
                operation="write",
            ),
            ToolDefinition(
                name="slack_send_alert",
                description="Send a proactive alert to the NOC or newsroom Slack channel",
                input_schema={
                    "type": "object",
                    "properties": {
                        "title":    {"type": "string"},
                        "message":  {"type": "string"},
                        "severity": {"type": "string", "enum": ["critical","warning","info","ok"]},
                        "channel":  {"type": "string"},
                    },
                    "required": ["title", "message"],
                },
                connector_id=self.connector_id,
                operation="write",
            ),
            ToolDefinition(
                name="slack_read_channel",
                description="Read recent messages from a Slack channel",
                input_schema={
                    "type": "object",
                    "properties": {
                        "channel": {"type": "string"},
                        "limit":   {"type": "integer", "default": 10},
                    },
                    "required": ["channel"],
                },
                connector_id=self.connector_id,
                operation="read",
            ),
        ]


# ─── Singleton instance ───────────────────────────────────────────────────────

slack_channel = SlackChannelConnector(demo_mode=True)
