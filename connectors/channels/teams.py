"""
MediaAgentIQ — Microsoft Teams Channel Connector

Bidirectional Teams integration via Bot Framework:
  INBOUND  — receives user messages via /teams/messages webhook
             (handled by gateway/webhook_handler.py)
  OUTBOUND — sends agent results as Adaptive Cards,
             sends proactive alerts via Bot Framework proactive messaging

Production requires:
  TEAMS_APP_ID        — Bot app registration ID (Azure AD)
  TEAMS_APP_PASSWORD  — Bot app registration password
  TEAMS_TENANT_ID     — Azure AD tenant ID (optional)

Demo mode:
  All send operations log to console instead of hitting Bot Framework.
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

logger = logging.getLogger("connector.teams")


class TeamsChannelConnector(BaseConnector):
    """
    Microsoft Teams Bot Framework connector.

    Agents call this connector to:
    - Send Adaptive Card responses to Teams conversations
    - Send proactive alerts to Teams channels
    - Update existing message cards (replace with final result)
    """

    def __init__(self, demo_mode: bool = True):
        from settings import settings as _settings
        super().__init__(ConnectorConfig(
            connector_id="teams",
            name="Microsoft Teams",
            category=ConnectorCategory.COMMS,
            auth_type=AuthType.OAUTH2,
            demo_mode=demo_mode,
            config={
                "app_id":       getattr(_settings, "TEAMS_APP_ID", ""),
                "app_password": getattr(_settings, "TEAMS_APP_PASSWORD", ""),
                "tenant_id":    getattr(_settings, "TEAMS_TENANT_ID", "common"),
            }
        ))
        self._token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None

    # ── Connection ─────────────────────────────────────────────────────

    async def authenticate(self) -> bool:
        if self.demo_mode:
            logger.info("Teams connector: DEMO mode — no real API calls")
            return True
        try:
            import httpx
            url = f"https://login.microsoftonline.com/{self.config.config['tenant_id']}/oauth2/v2.0/token"
            data = {
                "grant_type":    "client_credentials",
                "client_id":     self.config.config["app_id"],
                "client_secret": self.config.config["app_password"],
                "scope":         "https://api.botframework.com/.default",
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=data, timeout=15)
                response.raise_for_status()
                token_data = response.json()
                self._token = token_data["access_token"]
                logger.info("Teams Bot Framework token obtained")
                return True
        except Exception as e:
            logger.error(f"Teams auth failed: {e}")
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
            # Validate token is still fresh
            if not self._token:
                await self.authenticate()
            latency = (time.time() - start) * 1000
            self.last_health_check = HealthCheckResult(
                connector_id=self.connector_id,
                status=ConnectorStatus.CONNECTED,
                latency_ms=round(latency, 1),
                message="Teams Bot Framework token valid",
            )
        except Exception as e:
            self.last_health_check = HealthCheckResult(
                connector_id=self.connector_id,
                status=ConnectorStatus.ERROR,
                message=str(e),
            )
        return self.last_health_check

    # ── Core operations ────────────────────────────────────────────────

    async def read(self, params: Dict[str, Any]) -> Any:
        """Read is handled via incoming webhook — not polled."""
        return self._demo_response({"note": "Teams messages arrive via /teams/messages webhook"})

    async def write(self, data: Any, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Send an Adaptive Card or plain message to a Teams conversation.

        data: output from formatter.format_teams() — a Teams Activity dict
        params: {"service_url": "...", "conversation_id": "...", "activity_id": "..."}
        """
        params = params or {}
        if self.demo_mode:
            logger.info(f"[DEMO] Teams → {params.get('conversation_id','?')}: "
                        f"{str(data)[:120]}")
            return self._demo_response({"id": f"demo-{datetime.now().timestamp()}"})

        try:
            import httpx
            service_url = params.get("service_url", "https://smba.trafficmanager.net/amer/")
            conv_id = params.get("conversation_id", "")
            reply_to = params.get("activity_id", "")

            url = f"{service_url}v3/conversations/{conv_id}/activities"
            if reply_to:
                url += f"/{reply_to}"

            headers = {
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json",
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data, headers=headers, timeout=15)
                response.raise_for_status()
                return self._production_response(response.json())
        except Exception as e:
            logger.error(f"Teams write error: {e}")
            return self._error_response(str(e))

    # ── High-level helpers ─────────────────────────────────────────────

    async def send_activity(
        self,
        service_url: str,
        conversation_id: str,
        activity_id: str,
        payload: Dict,
    ) -> Dict:
        """Send a Bot Framework Activity (Adaptive Card or plain message)."""
        return await self.write(
            payload,
            {
                "service_url":     service_url,
                "conversation_id": conversation_id,
                "activity_id":     activity_id,
            }
        )

    async def send_alert(
        self,
        title: str,
        message: str,
        severity: str = "warning",
        conversation_id: str = None,
        service_url: str = None,
        agent: str = "",
    ) -> Dict:
        """Send a proactive alert card to a Teams channel."""
        color_map = {"critical": "attention", "warning": "warning", "info": "accent", "ok": "good"}
        color = color_map.get(severity, "default")

        card = {
            "type": "message",
            "attachments": [{
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": [
                        {"type": "TextBlock", "text": title, "size": "Large",
                         "weight": "Bolder", "color": color},
                        {"type": "TextBlock", "text": message, "wrap": True},
                        {"type": "TextBlock",
                         "text": f"MediaAgentIQ {agent} • {datetime.now().strftime('%H:%M:%S')}",
                         "size": "Small", "isSubtle": True},
                    ],
                }
            }]
        }
        return await self.write(
            card,
            {"service_url": service_url or "", "conversation_id": conversation_id or ""}
        )

    # ── MCP Tool Definitions ───────────────────────────────────────────

    def get_tool_definitions(self) -> List[ToolDefinition]:
        return [
            ToolDefinition(
                name="teams_send_message",
                description="Send an Adaptive Card or message to a Microsoft Teams conversation",
                input_schema={
                    "type": "object",
                    "properties": {
                        "conversation_id": {"type": "string"},
                        "service_url":     {"type": "string"},
                        "text":            {"type": "string"},
                        "adaptive_card":   {"type": "object"},
                    },
                    "required": ["conversation_id"],
                },
                connector_id=self.connector_id,
                operation="write",
            ),
            ToolDefinition(
                name="teams_send_alert",
                description="Send a proactive alert card to a Microsoft Teams channel",
                input_schema={
                    "type": "object",
                    "properties": {
                        "title":           {"type": "string"},
                        "message":         {"type": "string"},
                        "severity":        {"type": "string", "enum": ["critical","warning","info","ok"]},
                        "conversation_id": {"type": "string"},
                    },
                    "required": ["title", "message"],
                },
                connector_id=self.connector_id,
                operation="write",
            ),
        ]


# ─── Singleton instance ───────────────────────────────────────────────────────
# demo_mode is False when TEAMS_APP_ID is set in .env

def _resolve_demo_mode() -> bool:
    try:
        from settings import settings
        return not bool(settings.TEAMS_APP_ID)
    except Exception:
        return True

teams_channel = TeamsChannelConnector(demo_mode=_resolve_demo_mode())
