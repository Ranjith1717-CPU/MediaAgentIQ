"""
MediaAgentIQ — UserProfile (v3.3.0)

Reads memory/system/USER.md and exposes user preferences to the HOPE Engine.
Non-fatal: all methods return safe defaults if the file is missing or malformed.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from settings import Settings

logger = logging.getLogger(__name__)


class UserProfile:
    """Reads memory/system/USER.md and exposes user preferences."""

    def __init__(self, settings: "Settings") -> None:
        self._settings = settings
        mem_root = Path(settings.MEMORY_DIR)
        self._user_md = mem_root / "system" / "USER.md"

        # Parsed fields (populated by load())
        self._slack_handle: str = "@user"
        self._timezone: str = "UTC"
        self._digest_time: str = "08:00"
        self._mute_start: int = settings.HOPE_MUTE_START_HOUR
        self._mute_end: int = settings.HOPE_MUTE_END_HOUR
        self._max_alerts: int = settings.HOPE_MAX_ALERTS_PER_HOUR
        self._channels: dict = {
            "CRITICAL": "#breaking-alerts",
            "HIGH": "dm",
            "NORMAL": "#media-alerts",
            "LOW": "#media-alerts",
        }
        self._loaded: bool = False

    # ── Public interface ──────────────────────────────────────────────────────

    def load(self) -> None:
        """Parse USER.md. Creates the file from defaults if missing. Never raises."""
        try:
            if not self._user_md.exists():
                self._user_md.parent.mkdir(parents=True, exist_ok=True)
                self._user_md.write_text(self._default_user_md(), encoding="utf-8")
                logger.debug("UserProfile: Created default USER.md")

            content = self._user_md.read_text(encoding="utf-8")
            self._parse(content)
            self._loaded = True
        except Exception as e:
            logger.warning(f"UserProfile.load() failed (non-fatal): {e}")

    @property
    def slack_handle(self) -> str:
        return self._slack_handle

    @property
    def timezone(self) -> str:
        return self._timezone

    @property
    def digest_time(self) -> str:
        return self._digest_time

    def get_channel_for_priority(self, priority: str) -> str:
        """Return Slack channel string for the given alert priority."""
        return self._channels.get(priority.upper(), "#mediaagentiq")

    def is_muted(self, priority: str) -> bool:
        """
        Return True if current hour is inside quiet hours.
        CRITICAL always bypasses mute.
        """
        if priority.upper() == "CRITICAL":
            return False
        try:
            now_hour = datetime.now().hour
            start, end = self._mute_start, self._mute_end
            if start > end:  # crosses midnight
                return now_hour >= start or now_hour < end
            return start <= now_hour < end
        except Exception:
            return False

    # ── Internal ──────────────────────────────────────────────────────────────

    def _parse(self, content: str) -> None:
        """Extract structured fields from USER.md markdown."""
        def _find(pattern: str, default: str = "") -> str:
            m = re.search(pattern, content, re.IGNORECASE)
            return m.group(1).strip() if m else default

        self._slack_handle = _find(r"\*\*Slack Handle\*\*:\s*(\S+)", "@user")
        self._timezone = _find(r"\*\*Timezone\*\*:\s*(.+)", "UTC")
        self._digest_time = _find(r"\*\*Digest Time\*\*:\s*(\S+)", "08:00")

        # Parse notification channels block
        channel_block = re.search(
            r"\*\*Notification Channels\*\*:(.*?)(?=\n\*\*|\Z)", content,
            re.DOTALL
        )
        if channel_block:
            block = channel_block.group(1)
            priority_map = {"CRITICAL": "#breaking-alerts", "HIGH": "dm",
                            "NORMAL": "#media-alerts", "LOW": "#media-alerts"}
            for prio in ("CRITICAL", "HIGH", "NORMAL", "LOW"):
                m = re.search(
                    rf"{prio}\s*→\s*(.+)", block, re.IGNORECASE
                )
                if m:
                    priority_map[prio] = m.group(1).strip()
            self._channels = priority_map

        # Mute hours: "23:00–07:00 IST"
        mute_m = re.search(r"\*\*Mute Hours\*\*:\s*(\d+):\d+\D+(\d+):\d+", content)
        if mute_m:
            self._mute_start = int(mute_m.group(1))
            self._mute_end = int(mute_m.group(2))

        # Max alerts
        max_m = re.search(r"\*\*Max Alerts/Hour\*\*:\s*(\d+)", content)
        if max_m:
            self._max_alerts = int(max_m.group(1))

    @staticmethod
    def _default_user_md() -> str:
        return """\
# USER Profile — Default
_Standing preferences for HOPE Engine_

**Slack Handle**: @user
**Timezone**: UTC
**Notification Channels**:
- CRITICAL → Slack DM + @here in #breaking-alerts
- HIGH → Slack DM only
- NORMAL → #media-alerts channel
- LOW → digest only (no immediate alert)

**Mute Hours**: 23:00–07:00 (CRITICAL bypasses mute)
**Digest Time**: 08:00 daily
**Max Alerts/Hour**: 10 (non-critical)
"""
