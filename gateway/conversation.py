"""
MediaAgentIQ — Conversation Manager

Maintains per-user, per-channel conversation context so agents
can handle multi-turn interactions naturally.

Example multi-turn:
  User:  "Check compliance on the 6pm clip"
  Bot:   [Compliance card — score 72, 2 issues]
  User:  "Now translate it to Spanish"        ← knows "it" = same clip
  Bot:   [Localization card]
  User:  "Approve that"                       ← knows last pending action
  Bot:   [Confirmation]
"""

import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

logger = logging.getLogger("gateway.conversation")

# How long to keep a conversation session alive (minutes)
SESSION_TTL_MINUTES = 30


@dataclass
class Turn:
    """A single exchange in a conversation."""
    role: str                   # "user" | "agent"
    content: str
    agent_key: Optional[str] = None
    agent_result: Optional[Dict[str, Any]] = None
    params: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    message_ts: Optional[str] = None   # Slack message timestamp (for updates)
    channel: Optional[str] = None


@dataclass
class ConversationSession:
    """
    A conversation session for one user in one channel.
    Tracks turns, last active content URL, and pending actions.
    """
    user_id: str
    channel_id: str
    platform: str               # "slack" | "teams"
    turns: List[Turn] = field(default_factory=list)
    last_active: datetime = field(default_factory=datetime.now)

    # Context carried across turns
    last_url: Optional[str] = None          # last media URL mentioned
    last_agent_key: Optional[str] = None    # last agent invoked
    last_result: Optional[Dict] = None      # last agent result
    pending_action: Optional[Dict] = None   # awaiting user approval

    @property
    def is_expired(self) -> bool:
        return datetime.now() - self.last_active > timedelta(minutes=SESSION_TTL_MINUTES)

    def add_user_turn(
        self,
        content: str,
        agent_key: str = None,
        params: Dict = None,
        channel: str = None,
    ) -> Turn:
        turn = Turn(
            role="user",
            content=content,
            agent_key=agent_key,
            params=params or {},
            channel=channel,
        )
        self.turns.append(turn)
        self.last_active = datetime.now()
        if agent_key:
            self.last_agent_key = agent_key
        if params and params.get("url"):
            self.last_url = params["url"]
        return turn

    def add_agent_turn(
        self,
        agent_key: str,
        result: Dict[str, Any],
        message_ts: str = None,
        channel: str = None,
    ) -> Turn:
        turn = Turn(
            role="agent",
            content=f"{agent_key} completed",
            agent_key=agent_key,
            agent_result=result,
            message_ts=message_ts,
            channel=channel,
        )
        self.turns.append(turn)
        self.last_active = datetime.now()
        self.last_agent_key = agent_key
        self.last_result = result
        return turn

    def set_pending_action(self, action: Dict) -> None:
        """
        Store a pending action awaiting user approval.
        Used by AI Production Director and other approval-gate agents.
        Example: {"type": "approve_broadcast", "agent": "playout", "data": {...}}
        """
        self.pending_action = action

    def clear_pending_action(self) -> Optional[Dict]:
        action = self.pending_action
        self.pending_action = None
        return action

    def resolve_params(self, new_params: Dict) -> Dict:
        """
        Merge new params with context from previous turns.
        Fills in missing URL from last known URL, etc.
        """
        resolved = dict(new_params)
        if not resolved.get("url") and self.last_url:
            resolved["url"] = self.last_url
        return resolved

    def get_history_for_llm(self) -> List[Dict[str, str]]:
        """Return recent turns in OpenAI message format for LLM routing."""
        history = []
        for turn in self.turns[-6:]:   # last 6 turns
            role = "user" if turn.role == "user" else "assistant"
            history.append({"role": role, "content": turn.content})
        return history


class ConversationManager:
    """
    Registry of active conversation sessions.
    Session key = (platform, channel_id, user_id)
    """

    def __init__(self):
        # sessions[(platform, channel_id, user_id)] = ConversationSession
        self._sessions: Dict[tuple, ConversationSession] = {}

    def _key(self, platform: str, channel_id: str, user_id: str) -> tuple:
        return (platform, channel_id, user_id)

    def get_or_create(
        self,
        platform: str,
        channel_id: str,
        user_id: str,
    ) -> ConversationSession:
        key = self._key(platform, channel_id, user_id)
        session = self._sessions.get(key)

        if session is None or session.is_expired:
            session = ConversationSession(
                user_id=user_id,
                channel_id=channel_id,
                platform=platform,
            )
            self._sessions[key] = session
            logger.debug(f"New conversation session: {platform}/{channel_id}/{user_id}")

        return session

    def get(
        self,
        platform: str,
        channel_id: str,
        user_id: str,
    ) -> Optional[ConversationSession]:
        key = self._key(platform, channel_id, user_id)
        session = self._sessions.get(key)
        if session and not session.is_expired:
            return session
        return None

    def cleanup_expired(self) -> int:
        """Remove expired sessions. Returns number removed."""
        expired = [k for k, v in self._sessions.items() if v.is_expired]
        for k in expired:
            del self._sessions[k]
        if expired:
            logger.info(f"Cleaned up {len(expired)} expired sessions")
        return len(expired)

    @property
    def active_session_count(self) -> int:
        return sum(1 for s in self._sessions.values() if not s.is_expired)


# Global singleton
conversation_manager = ConversationManager()
