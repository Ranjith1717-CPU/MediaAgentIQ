"""
MediaAgentIQ — Base Connector

Foundation for all connector implementations.

Connectors are the integration layer of MediaAgentIQ — they expose
external systems as MCP-style tools that agents can discover and call.

Every connector provides:
  authenticate()          — establish authenticated session
  health_check()          — verify connection is live
  read(params)            — pull data from external system
  write(data, params)     — push data to external system
  subscribe(event, cb)    — register for event callbacks (webhooks/WS)
  get_tool_definitions()  — MCP-style tool schema for agent discovery

Connectors operate in two modes (mirrors agent dual-mode):
  Demo mode     — realistic mock responses, no real credentials needed
  Production    — real API/SDK calls with proper authentication
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import logging


# ─────────────────────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────────────────────

class ConnectorStatus(str, Enum):
    CONNECTED     = "connected"
    DISCONNECTED  = "disconnected"
    ERROR         = "error"
    AUTHENTICATING = "authenticating"
    DEGRADED      = "degraded"


class ConnectorCategory(str, Enum):
    STORAGE       = "storage"
    MAM           = "mam"
    NEWSROOM      = "newsroom"
    PLAYOUT       = "playout"
    SOCIAL        = "social"
    ADTECH        = "adtech"
    COMMS         = "comms"
    CDN           = "cdn"
    TRANSCODING   = "transcoding"
    ANALYTICS     = "analytics"
    MONITORING    = "monitoring"
    WIRE_SERVICES = "wire_services"
    NLE           = "nle"
    GRAPHICS      = "graphics"


class AuthType(str, Enum):
    API_KEY     = "api_key"
    OAUTH2      = "oauth2"
    BASIC       = "basic"
    CERTIFICATE = "certificate"
    TOKEN       = "token"
    NONE        = "none"


# ─────────────────────────────────────────────────────────────
# Config dataclass
# ─────────────────────────────────────────────────────────────

@dataclass
class ConnectorConfig:
    """Configuration for a connector instance."""
    connector_id: str
    name: str
    category: ConnectorCategory
    auth_type: AuthType
    config: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    demo_mode: bool = True          # mirrors PRODUCTION_MODE=False
    timeout_seconds: int = 30
    retry_attempts: int = 3
    tags: List[str] = field(default_factory=list)


# ─────────────────────────────────────────────────────────────
# Tool definition (MCP-style)
# ─────────────────────────────────────────────────────────────

@dataclass
class ToolDefinition:
    """
    MCP-style tool definition.

    Agents use these to discover what operations a connector supports.
    Schema follows Anthropic tool-use format so definitions can be
    passed directly into Claude API calls.
    """
    name: str
    description: str
    input_schema: Dict[str, Any]
    connector_id: str
    operation: str      # "read" | "write" | "subscribe"
    requires_auth: bool = True

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
            "connector_id": self.connector_id,
            "operation": self.operation,
            "requires_auth": self.requires_auth,
        }


# ─────────────────────────────────────────────────────────────
# Health check result
# ─────────────────────────────────────────────────────────────

@dataclass
class HealthCheckResult:
    connector_id: str
    status: ConnectorStatus
    latency_ms: Optional[float] = None
    message: str = ""
    checked_at: datetime = field(default_factory=datetime.now)
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "connector_id": self.connector_id,
            "status": self.status.value,
            "latency_ms": self.latency_ms,
            "message": self.message,
            "checked_at": self.checked_at.isoformat(),
            "details": self.details,
        }


# ─────────────────────────────────────────────────────────────
# Base Connector
# ─────────────────────────────────────────────────────────────

class BaseConnector(ABC):
    """
    Abstract base class for all MediaAgentIQ connectors.

    Subclasses must implement:
      authenticate(), health_check(), read(), write()

    Optionally override:
      subscribe(), disconnect(), get_tool_definitions()
    """

    def __init__(self, config: ConnectorConfig):
        self.config = config
        self.connector_id = config.connector_id
        self.name = config.name
        self.category = config.category
        self.demo_mode = config.demo_mode

        self.status = ConnectorStatus.DISCONNECTED
        self._connected = False
        self.last_health_check: Optional[HealthCheckResult] = None
        self.connected_at: Optional[datetime] = None
        self.error_count: int = 0
        self.request_count: int = 0

        self._subscriptions: Dict[str, List[Callable]] = {}

        self.logger = logging.getLogger(f"connector.{self.connector_id}")

    # ── Properties ──────────────────────────────────────────

    @property
    def is_connected(self) -> bool:
        return self._connected and self.status == ConnectorStatus.CONNECTED

    @property
    def is_demo(self) -> bool:
        return self.demo_mode

    # ── Abstract methods ────────────────────────────────────

    @abstractmethod
    async def authenticate(self) -> bool:
        """
        Establish authenticated connection to the external system.
        Returns True if successful.
        In demo mode: always returns True.
        In production: validates credentials and obtains session/token.
        """

    @abstractmethod
    async def health_check(self) -> HealthCheckResult:
        """
        Verify the connector is live and responsive.
        Should update self.last_health_check and self.status.
        """

    @abstractmethod
    async def read(self, params: Dict[str, Any]) -> Any:
        """
        Pull data from the external system.
        params is connector-specific.
        """

    @abstractmethod
    async def write(self, data: Any, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Push data to the external system.
        Returns a result dict with at minimum {"success": bool}.
        """

    # ── Optional overrides ──────────────────────────────────

    async def subscribe(self, event: str, callback: Callable) -> str:
        """
        Register a callback for an event (webhooks / websockets).
        Returns a subscription ID.
        Override in connectors that support event streaming.
        """
        raise NotImplementedError(
            f"{self.name} does not support event subscriptions. "
            "Override subscribe() to enable this."
        )

    async def disconnect(self) -> None:
        """Close the connection gracefully."""
        self._connected = False
        self.status = ConnectorStatus.DISCONNECTED
        self.logger.info(f"{self.name} disconnected")

    def get_tool_definitions(self) -> List[ToolDefinition]:
        """
        Return MCP-style tool definitions for this connector.

        Override in subclasses to expose specific operations as tools
        that agents can discover and call.

        Default returns empty list (connector has no declared tools).
        """
        return []

    # ── Lifecycle ───────────────────────────────────────────

    async def connect(self) -> bool:
        """Authenticate and mark as connected."""
        self.status = ConnectorStatus.AUTHENTICATING
        self.logger.info(f"Connecting to {self.name} (demo={self.demo_mode})")

        success = await self.authenticate()

        if success:
            self.status = ConnectorStatus.CONNECTED
            self._connected = True
            self.connected_at = datetime.now()
            self.logger.info(f"{self.name} connected successfully")
        else:
            self.status = ConnectorStatus.ERROR
            self.error_count += 1
            self.logger.error(f"{self.name} authentication failed")

        return success

    # ── Utility ─────────────────────────────────────────────

    def get_info(self) -> Dict[str, Any]:
        """Return connector metadata."""
        return {
            "connector_id": self.connector_id,
            "name": self.name,
            "category": self.category.value,
            "status": self.status.value,
            "demo_mode": self.demo_mode,
            "connected": self._connected,
            "connected_at": self.connected_at.isoformat() if self.connected_at else None,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "last_health_check": self.last_health_check.to_dict() if self.last_health_check else None,
            "tools": [t.name for t in self.get_tool_definitions()],
        }

    def _demo_response(self, data: Any) -> Dict[str, Any]:
        """Wrap demo data in a standard response envelope."""
        return {
            "success": True,
            "connector": self.connector_id,
            "mode": "demo",
            "timestamp": datetime.now().isoformat(),
            "data": data,
        }

    def _production_response(self, data: Any, raw: Any = None) -> Dict[str, Any]:
        """Wrap production data in a standard response envelope."""
        self.request_count += 1
        return {
            "success": True,
            "connector": self.connector_id,
            "mode": "production",
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "raw": raw,
        }

    def _error_response(self, error: str) -> Dict[str, Any]:
        self.error_count += 1
        return {
            "success": False,
            "connector": self.connector_id,
            "mode": "demo" if self.demo_mode else "production",
            "timestamp": datetime.now().isoformat(),
            "error": error,
        }


# ─────────────────────────────────────────────────────────────
# Exceptions
# ─────────────────────────────────────────────────────────────

class ConnectorAuthError(Exception):
    def __init__(self, connector_id: str, reason: str):
        super().__init__(f"[{connector_id}] Authentication failed: {reason}")
        self.connector_id = connector_id


class ConnectorNotConnectedError(Exception):
    def __init__(self, connector_id: str):
        super().__init__(
            f"[{connector_id}] Not connected. Call connect() first."
        )
        self.connector_id = connector_id


class ConnectorOperationError(Exception):
    def __init__(self, connector_id: str, operation: str, reason: str):
        super().__init__(f"[{connector_id}] {operation} failed: {reason}")
        self.connector_id = connector_id
