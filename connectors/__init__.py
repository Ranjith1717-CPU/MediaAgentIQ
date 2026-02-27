"""
MediaAgentIQ Connector Framework

Two connector families:

  Channel Connectors (user-facing — bidirectional):
    slack   — Slack Bot (slash commands, @mentions, Block Kit cards)
    teams   — Microsoft Teams Bot (Adaptive Cards)

  System Connectors (backend integrations):
    s3, avid, harmonic, cloudfront, ffmpeg, inews, ...
    (registered as needed per deployment)

Usage:
    from connectors.registry import connector_registry

    # Get a connector
    slack = connector_registry.get("slack")
    await slack.send_alert("Signal quality critical", "Stream X dropped", severity="critical")

    # MCP tool call
    result = await connector_registry.call_tool(
        "slack_send_message",
        {"channel": "#newsroom", "text": "Rundown synced"}
    )

    # Connect all at startup
    from connectors import setup_connectors
    await setup_connectors(demo_mode=True)
"""

from connectors.registry import connector_registry, setup_default_connectors
from connectors.base_connector import (
    BaseConnector,
    ConnectorConfig,
    ConnectorCategory,
    ConnectorStatus,
    AuthType,
    ToolDefinition,
    HealthCheckResult,
)


def register_all_connectors(registry=None, demo_mode: bool = True) -> None:
    """
    Register all default connectors with the registry.
    Called at application startup.
    """
    if registry is None:
        registry = connector_registry

    # Channel connectors (always registered — user-facing UI)
    from connectors.channels.slack import SlackChannelConnector
    from connectors.channels.teams import TeamsChannelConnector

    slack = SlackChannelConnector(demo_mode=demo_mode)
    teams = TeamsChannelConnector(demo_mode=demo_mode)

    slack.config.enabled = True
    teams.config.enabled = True

    registry.register(slack)
    registry.register(teams)


async def setup_connectors(demo_mode: bool = True):
    """Register and connect all default connectors. Call at app startup."""
    register_all_connectors(connector_registry, demo_mode=demo_mode)
    await connector_registry.connect_all()
    return connector_registry


__all__ = [
    "connector_registry",
    "setup_connectors",
    "register_all_connectors",
    "setup_default_connectors",
    "BaseConnector",
    "ConnectorConfig",
    "ConnectorCategory",
    "ConnectorStatus",
    "AuthType",
    "ToolDefinition",
    "HealthCheckResult",
]
