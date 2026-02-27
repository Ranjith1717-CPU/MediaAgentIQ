"""
MediaAgentIQ — Channel Connectors

User-facing channel connectors. These are the UI surfaces where
broadcast staff interact with agents directly.

Supported channels:
  slack  — Slack Bot (slash commands + @mentions + Block Kit cards)
  teams  — Microsoft Teams Bot (Adaptive Cards)

Both are bidirectional:
  INBOUND  — users send commands, agents receive and process
  OUTBOUND — agents send results, proactive alerts, interactive cards
"""
from connectors.channels.slack import SlackChannelConnector, slack_channel
from connectors.channels.teams import TeamsChannelConnector, teams_channel

__all__ = [
    "SlackChannelConnector",
    "slack_channel",
    "TeamsChannelConnector",
    "teams_channel",
]
