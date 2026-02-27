"""
MediaAgentIQ — Connector Registry

Central hub for connector discovery, lifecycle management,
and MCP-style tool exposure.

Usage:
    from connectors import connector_registry

    # Get a specific connector
    slack = connector_registry.get("slack")
    await slack.write({"channel": "#noc", "message": "Alert!"})

    # Get all connectors for a category
    storage = connector_registry.get_by_category(ConnectorCategory.STORAGE)

    # MCP-style: discover all available tools
    tools = connector_registry.get_all_tool_definitions()

    # Connect all registered connectors
    await connector_registry.connect_all()

    # Dashboard
    dashboard = connector_registry.get_dashboard()
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from .base_connector import (
    BaseConnector,
    ConnectorCategory,
    ConnectorStatus,
    HealthCheckResult,
    ToolDefinition,
)

logger = logging.getLogger("connector.registry")


class ConnectorRegistry:
    """
    Central registry for all MediaAgentIQ connectors.

    Responsibilities:
    - Register / deregister connectors
    - Lifecycle management (connect, disconnect, reconnect)
    - Health monitoring (periodic checks)
    - MCP tool discovery (aggregate tool definitions from all connectors)
    - Category-based lookup for agents
    """

    def __init__(self):
        self._connectors: Dict[str, BaseConnector] = {}
        self._categories: Dict[ConnectorCategory, List[str]] = {
            cat: [] for cat in ConnectorCategory
        }
        self._tool_index: Dict[str, ToolDefinition] = {}   # tool_name → ToolDefinition
        self._health_history: Dict[str, List[HealthCheckResult]] = {}

        self.created_at = datetime.now()
        self.stats = {
            "total_registered": 0,
            "total_connected": 0,
            "health_checks_run": 0,
        }

        logger.info("ConnectorRegistry initialized")

    # ─── Registration ─────────────────────────────────────────────────

    def register(self, connector: BaseConnector) -> None:
        """
        Register a connector with the registry.

        Also indexes its tool definitions for MCP discovery.
        """
        cid = connector.connector_id

        if cid in self._connectors:
            logger.warning(f"Connector '{cid}' already registered — replacing")

        self._connectors[cid] = connector
        self._categories[connector.category].append(cid)
        self._health_history[cid] = []

        # Index tool definitions
        for tool in connector.get_tool_definitions():
            self._tool_index[tool.name] = tool

        self.stats["total_registered"] += 1
        logger.info(
            f"Registered connector: {cid} "
            f"(category={connector.category.value}, "
            f"demo={connector.demo_mode}, "
            f"tools={len(connector.get_tool_definitions())})"
        )

    def deregister(self, connector_id: str) -> bool:
        """Remove a connector from the registry."""
        if connector_id not in self._connectors:
            return False

        connector = self._connectors[connector_id]

        # Remove from category index
        cat_list = self._categories.get(connector.category, [])
        if connector_id in cat_list:
            cat_list.remove(connector_id)

        # Remove tools
        for tool in connector.get_tool_definitions():
            self._tool_index.pop(tool.name, None)

        del self._connectors[connector_id]
        logger.info(f"Deregistered connector: {connector_id}")
        return True

    # ─── Lookup ───────────────────────────────────────────────────────

    def get(self, connector_id: str) -> Optional[BaseConnector]:
        """Get a connector by ID. Returns None if not found."""
        return self._connectors.get(connector_id)

    def get_by_category(self, category: ConnectorCategory) -> List[BaseConnector]:
        """Get all connectors for a category (connected or not)."""
        ids = self._categories.get(category, [])
        return [self._connectors[cid] for cid in ids if cid in self._connectors]

    def get_connected(self) -> List[BaseConnector]:
        """Return only connectors that are currently connected."""
        return [c for c in self._connectors.values() if c.is_connected]

    def list_ids(self) -> List[str]:
        """Return all registered connector IDs."""
        return list(self._connectors.keys())

    # ─── Lifecycle ────────────────────────────────────────────────────

    async def connect_all(self) -> Dict[str, bool]:
        """
        Connect all enabled connectors concurrently.
        Returns dict of connector_id → success.
        """
        enabled = [c for c in self._connectors.values() if c.config.enabled]
        logger.info(f"Connecting {len(enabled)} connectors...")

        results = await asyncio.gather(
            *[c.connect() for c in enabled],
            return_exceptions=True
        )

        outcome: Dict[str, bool] = {}
        for connector, result in zip(enabled, results):
            if isinstance(result, Exception):
                outcome[connector.connector_id] = False
                logger.error(f"Failed to connect {connector.connector_id}: {result}")
            else:
                outcome[connector.connector_id] = result

        connected = sum(v for v in outcome.values())
        self.stats["total_connected"] = connected
        logger.info(f"Connected {connected}/{len(enabled)} connectors")
        return outcome

    async def disconnect_all(self) -> None:
        """Disconnect all connectors gracefully."""
        await asyncio.gather(*[c.disconnect() for c in self._connectors.values()])
        logger.info("All connectors disconnected")

    async def reconnect(self, connector_id: str) -> bool:
        """Disconnect then reconnect a specific connector."""
        connector = self.get(connector_id)
        if not connector:
            return False
        await connector.disconnect()
        return await connector.connect()

    # ─── Health monitoring ────────────────────────────────────────────

    async def health_check_all(self) -> Dict[str, HealthCheckResult]:
        """
        Run health checks on all connected connectors concurrently.
        Stores last 50 results per connector for trend analysis.
        """
        connected = self.get_connected()
        results_list = await asyncio.gather(
            *[c.health_check() for c in connected],
            return_exceptions=True
        )

        results: Dict[str, HealthCheckResult] = {}
        for connector, result in zip(connected, results_list):
            cid = connector.connector_id
            if isinstance(result, Exception):
                result = HealthCheckResult(
                    connector_id=cid,
                    status=ConnectorStatus.ERROR,
                    message=str(result),
                )

            # Store history (keep last 50)
            history = self._health_history.setdefault(cid, [])
            history.append(result)
            if len(history) > 50:
                history.pop(0)

            results[cid] = result

        self.stats["health_checks_run"] += 1
        return results

    async def health_check(self, connector_id: str) -> Optional[HealthCheckResult]:
        """Run health check on a single connector."""
        connector = self.get(connector_id)
        if not connector:
            return None
        return await connector.health_check()

    # ─── MCP Tool Discovery ───────────────────────────────────────────

    def get_all_tool_definitions(self) -> List[ToolDefinition]:
        """
        Return all tool definitions from all registered connectors.

        This is the MCP discovery endpoint — pass these to an LLM
        to let it decide which connector operations to call.
        """
        return list(self._tool_index.values())

    def get_tool_definitions_for_category(
        self, category: ConnectorCategory
    ) -> List[ToolDefinition]:
        """Return tool definitions for connectors in a specific category."""
        connectors = self.get_by_category(category)
        tools = []
        for c in connectors:
            tools.extend(c.get_tool_definitions())
        return tools

    def get_tool(self, tool_name: str) -> Optional[ToolDefinition]:
        """Look up a tool definition by name."""
        return self._tool_index.get(tool_name)

    async def call_tool(
        self, tool_name: str, tool_input: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a tool by name with given input.

        This is the MCP tool-call entry point.
        Agents call this to execute connector operations without
        knowing which connector implements the tool.

        Example:
            result = await connector_registry.call_tool(
                "slack_send_message",
                {"channel": "#noc", "message": "Signal drop detected"}
            )
        """
        tool_def = self._tool_index.get(tool_name)
        if not tool_def:
            return {"success": False, "error": f"Unknown tool: {tool_name}"}

        connector = self.get(tool_def.connector_id)
        if not connector:
            return {"success": False, "error": f"Connector not found: {tool_def.connector_id}"}

        if not connector.is_connected:
            # Attempt auto-reconnect
            logger.info(f"Auto-connecting {tool_def.connector_id} for tool call")
            connected = await connector.connect()
            if not connected:
                return {
                    "success": False,
                    "error": f"Connector {tool_def.connector_id} not connected",
                }

        try:
            if tool_def.operation == "read":
                return await connector.read(tool_input)
            elif tool_def.operation == "write":
                data = tool_input.pop("data", tool_input)
                return await connector.write(data, tool_input)
            elif tool_def.operation == "subscribe":
                raise NotImplementedError("subscribe via call_tool not supported")
            else:
                return {"success": False, "error": f"Unknown operation: {tool_def.operation}"}
        except Exception as e:
            logger.error(f"Tool call failed [{tool_name}]: {e}")
            return {"success": False, "error": str(e)}

    # ─── Dashboard ────────────────────────────────────────────────────

    def get_dashboard(self) -> Dict[str, Any]:
        """
        Return a full status dashboard of all connectors.
        Used by Streamlit UI and the NOC Monitoring agent.
        """
        by_category: Dict[str, List[Dict]] = {}
        for cat in ConnectorCategory:
            connectors = self.get_by_category(cat)
            if connectors:
                by_category[cat.value] = [c.get_info() for c in connectors]

        connected_count = len(self.get_connected())
        total_count = len(self._connectors)

        return {
            "summary": {
                "total": total_count,
                "connected": connected_count,
                "disconnected": total_count - connected_count,
                "health_pct": round(connected_count / total_count * 100) if total_count else 0,
            },
            "by_category": by_category,
            "total_tools": len(self._tool_index),
            "tool_names": list(self._tool_index.keys()),
            "stats": self.stats,
            "uptime_seconds": (datetime.now() - self.created_at).total_seconds(),
        }

    def get_status_summary(self) -> str:
        """Return a one-line status summary."""
        connected = len(self.get_connected())
        total = len(self._connectors)
        tools = len(self._tool_index)
        return f"{connected}/{total} connectors live | {tools} MCP tools available"


# ─── Global singleton ─────────────────────────────────────────────────────────

connector_registry = ConnectorRegistry()


async def setup_default_connectors(demo_mode: bool = True) -> ConnectorRegistry:
    """
    Register and connect all default connectors.
    Called at application startup.
    """
    from connectors import register_all_connectors
    register_all_connectors(connector_registry, demo_mode=demo_mode)
    await connector_registry.connect_all()
    logger.info(connector_registry.get_status_summary())
    return connector_registry
