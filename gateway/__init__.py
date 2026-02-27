"""
MediaAgentIQ — Conversational Gateway

The gateway is the intelligence layer between user channels (Slack, Teams)
and the underlying agent platform.

Components:
  router.py          — Routes user messages to agents (NLP + slash commands)
  formatter.py       — Converts agent output to Slack Block Kit / Teams Adaptive Cards
  conversation.py    — Per-user conversation context across multi-turn exchanges
  webhook_handler.py — FastAPI routes for Slack Events API and Teams Bot Framework

Entry points:
  Mount gateway_router in app.py:
    from gateway.webhook_handler import gateway_router
    app.include_router(gateway_router)

  Slack slash command endpoints:
    POST /slack/events    — Events API (app_mention, message)
    POST /slack/commands  — Slash commands (/miq-*)
    POST /slack/actions   — Button / interactive component callbacks

  Teams endpoint:
    POST /teams/messages  — Bot Framework Activity handler

  Health check:
    GET  /gateway/health
"""
from gateway.router import route, RoutedIntent, HELP_TEXT
from gateway.conversation import conversation_manager, ConversationSession
from gateway.formatter import format_slack, format_teams, format_slack_error

__all__ = [
    "route",
    "RoutedIntent",
    "HELP_TEXT",
    "conversation_manager",
    "ConversationSession",
    "format_slack",
    "format_teams",
    "format_slack_error",
]
