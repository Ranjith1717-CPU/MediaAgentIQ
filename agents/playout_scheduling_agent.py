"""
Playout & Scheduling Agent

Manages the linear broadcast schedule and automation server integration:
- Schedule management (daily playlist / rundown)
- Broadcast automation system integration (Harmonic Polaris, GV Maestro)
- SCTE-35 ad break cue injection
- Commercial break timing optimisation
- Emergency / breaking news rundown interruption
- Live-to-tape switching

Demo mode: returns mock playout schedule and automation commands
Production mode: integrates with Harmonic / GV Maestro REST APIs
"""

import asyncio
import logging
import random
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .base_agent import BaseAgent, ProductionNotReadyError

if TYPE_CHECKING:
    from settings import Settings

logger = logging.getLogger(__name__)


def _tc(dt: datetime) -> str:
    """Format datetime as broadcast timecode HH:MM:SS:FF."""
    return dt.strftime("%H:%M:%S") + ":00"


ITEM_TYPES = ["segment", "commercial_break", "promo", "live_feed", "vod", "station_id"]
STATUSES   = ["ready", "ready", "ready", "cued", "warning"]


class PlayoutSchedulingAgent(BaseAgent):
    """
    Agent for managing broadcast playout schedules and automation servers.

    Demo Mode:  Returns realistic mock schedule with items, breaks, warnings
    Production: Connects to Harmonic Polaris or GV Maestro via REST API
    """

    def __init__(self, settings: Optional["Settings"] = None):
        super().__init__(
            name="Playout & Scheduling Agent",
            description=(
                "Broadcast playout schedule management — "
                "automation server integration, SCTE-35 break injection, "
                "and emergency rundown management"
            ),
            settings=settings,
        )

    async def validate_input(self, input_data: Any) -> bool:
        if isinstance(input_data, dict):
            return True  # mode / date optional
        return isinstance(input_data, str)

    async def _demo_process(self, input_data: Any) -> Dict[str, Any]:
        await asyncio.sleep(0.3)

        mode = (input_data.get("mode", "schedule") if isinstance(input_data, dict) else "schedule")
        target_date = datetime.now().date().isoformat()

        # Generate a realistic 24-hour playout schedule (sample of next 12 items)
        now = datetime.now().replace(second=0, microsecond=0)
        schedule_items = []
        cursor = now.replace(minute=0)

        item_templates = [
            {"title": "Evening News Bulletin",   "type": "segment",          "duration_min": 30},
            {"title": "Commercial Break 1",      "type": "commercial_break", "duration_min": 3},
            {"title": "Weather & Sport",         "type": "segment",          "duration_min": 10},
            {"title": "Commercial Break 2",      "type": "commercial_break", "duration_min": 2},
            {"title": "Late Night Talk Show",    "type": "segment",          "duration_min": 60},
            {"title": "Station Promo",           "type": "promo",            "duration_min": 1},
            {"title": "Live Press Conference",   "type": "live_feed",        "duration_min": 45},
            {"title": "Commercial Break 3",      "type": "commercial_break", "duration_min": 3},
            {"title": "Documentary: Nature",     "type": "vod",              "duration_min": 55},
            {"title": "Station ID",              "type": "station_id",       "duration_min": 0},
            {"title": "Overnight News",          "type": "segment",          "duration_min": 30},
            {"title": "Commercial Break 4",      "type": "commercial_break", "duration_min": 2},
        ]

        warnings = []
        for i, template in enumerate(item_templates):
            dur = timedelta(minutes=template["duration_min"])
            status = random.choice(STATUSES)
            has_warning = status == "warning"

            item = {
                "slot":       i + 1,
                "timecode":   _tc(cursor),
                "title":      template["title"],
                "type":       template["type"],
                "duration":   f"{template['duration_min']:02d}:00",
                "asset_id":   f"AVID-{random.randint(100000, 999999)}" if template["type"] != "live_feed" else "LIVE",
                "status":     status,
                "scte35":     template["type"] == "commercial_break",
                "warning":    has_warning,
            }
            schedule_items.append(item)

            if has_warning:
                warnings.append({
                    "slot":    i + 1,
                    "title":   template["title"],
                    "issue":   random.choice([
                        "Asset not yet ingested",
                        "Duration mismatch (±5s)",
                        "Missing audio track",
                        "Rights window closes in 2 hours",
                    ])
                })

            cursor += dur

        next_break = next(
            (f"{i['timecode']} — {i['title']}" for i in schedule_items if i["type"] == "commercial_break"),
            "N/A"
        )

        # Determine automation server status
        automation_server = random.choice(["Harmonic Polaris", "GV Maestro", "Ross Overdrive"])
        server_status = "online"

        return self.create_response(
            success=True,
            data={
                "date":               target_date,
                "total_items":        len(schedule_items),
                "schedule":           schedule_items,
                "warnings":           warnings,
                "warning_count":      len(warnings),
                "next_break":         next_break,
                "automation_server":  automation_server,
                "server_status":      server_status,
                "on_air_item":        schedule_items[0] if schedule_items else None,
                "scte35_breaks":      sum(1 for i in schedule_items if i["scte35"]),
                "total_ad_minutes":   sum(
                    int(i["duration"].split(":")[0])
                    for i in schedule_items if i["type"] == "commercial_break"
                ),
                "generated_at":       datetime.now().isoformat(),
            },
            metadata={"mode": "demo", "automation": automation_server},
        )

    async def _production_process(self, input_data: Any) -> Dict[str, Any]:
        """
        Production: connect to Harmonic Polaris or GV Maestro REST API
        and retrieve / update the live playout schedule.
        """
        automation_url = getattr(self.settings, "AUTOMATION_SERVER_URL", None)
        automation_type = getattr(self.settings, "AUTOMATION_SERVER_TYPE", "harmonic")

        if not automation_url:
            raise ProductionNotReadyError(self.name, "AUTOMATION_SERVER_URL")

        try:
            import httpx
            mode = input_data.get("mode", "get_schedule") if isinstance(input_data, dict) else "get_schedule"

            async with httpx.AsyncClient(timeout=15) as client:
                if automation_type == "harmonic":
                    endpoint = f"{automation_url}/api/v1/schedule/today"
                else:
                    endpoint = f"{automation_url}/schedule/current"

                response = await client.get(endpoint)
                response.raise_for_status()
                schedule_data = response.json()

            return self.create_response(
                success=True,
                data={
                    "automation_server": automation_type,
                    "schedule":          schedule_data.get("items", []),
                    "total_items":       len(schedule_data.get("items", [])),
                    "retrieved_at":      datetime.now().isoformat(),
                },
                metadata={"mode": "production", "automation": automation_type},
            )
        except Exception as e:
            logger.error(f"Playout schedule retrieval failed: {e}", exc_info=True)
            return self.create_response(success=False, error=str(e))
