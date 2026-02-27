"""
Newsroom Integration Agent

Bridges the editorial and technical broadcast workflow:
- Bi-directional sync with iNews / ENPS / Octopus via MOS protocol
- Wire service ingestion (AP, Reuters, AFP)
- Rundown to playout hand-off
- Story assignment and slot management
- Breaking news rundown interruption
- Shot list generation from story scripts

Demo mode: returns mock rundown with stories, wires, and MOS objects
Production mode: connects to iNews REST API / MOS over TCP
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


STORY_CATEGORIES = ["Politics", "Business", "Technology", "Crime", "Health",
                    "Weather", "Sports", "Entertainment", "International"]

STORY_STATUSES = ["filed", "editing", "approved", "ready", "on_air"]

WIRE_SOURCES = ["AP", "Reuters", "AFP", "Bloomberg", "PA Media"]


class NewsroomIntegrationAgent(BaseAgent):
    """
    Agent for newsroom system integration and rundown management.

    Demo Mode:  Returns realistic mock rundown with stories and wire copy
    Production: Connects to iNews via REST API or MOS protocol over TCP
    """

    def __init__(self, settings: Optional["Settings"] = None):
        super().__init__(
            name="Newsroom Integration Agent",
            description=(
                "Bi-directional newsroom sync — iNews/ENPS/Octopus MOS integration, "
                "wire service ingestion, rundown management, and playout hand-off"
            ),
            settings=settings,
        )

    async def validate_input(self, input_data: Any) -> bool:
        if isinstance(input_data, dict):
            return True
        return isinstance(input_data, str)

    async def _demo_process(self, input_data: Any) -> Dict[str, Any]:
        await asyncio.sleep(0.3)

        mode = (input_data.get("mode", "get_rundown") if isinstance(input_data, dict) else "get_rundown")
        show_name = (input_data.get("show", "Evening News") if isinstance(input_data, dict) else "Evening News")
        system = random.choice(["iNews", "ENPS", "Octopus"])

        now = datetime.now().replace(second=0, microsecond=0)

        # Generate rundown items
        story_titles = [
            "Prime Minister addresses parliament over budget crisis",
            "Tech giant announces major layoffs amid AI restructuring",
            "City hospital overwhelmed — winter surge continues",
            "Breaking: Earthquake strikes coastal region",
            "Local sports team secures championship spot",
            "New climate policy unveiled by energy minister",
            "Stock markets fall on inflation data",
            "Weather: Major storm system approaching this weekend",
            "Entertainment: Film festival opens to record crowds",
            "International: Peace talks resume in Geneva",
        ]
        random.shuffle(story_titles)

        rundown_items = []
        cursor = now.replace(hour=18, minute=0)  # 6pm show

        for i, title in enumerate(story_titles[:8]):
            dur_min = random.randint(1, 8)
            status = random.choice(STORY_STATUSES)
            category = random.choice(STORY_CATEGORIES)
            reporter = random.choice([
                "Sarah Mitchell", "James O'Brien", "Priya Sharma",
                "Tom Williams", "Laura Chen", "David Okafor"
            ])

            item = {
                "slot":         i + 1,
                "slug":         title[:12].replace(" ", "_").upper(),
                "title":        title,
                "category":     category,
                "reporter":     reporter,
                "duration":     f"{dur_min:02d}:00",
                "timecode":     cursor.strftime("%H:%M:%S"),
                "status":       status,
                "has_video":    random.choice([True, True, False]),
                "has_script":   status in ("editing", "approved", "ready", "on_air"),
                "mos_object_id": f"MOS-{random.randint(10000, 99999)}",
                "wire_source":  random.choice(WIRE_SOURCES) if random.random() > 0.5 else None,
            }
            rundown_items.append(item)
            cursor += timedelta(minutes=dur_min)

        # Latest wire stories
        wire_stories = []
        for i in range(5):
            priority = random.choice(["URGENT", "ROUTINE", "BULLETIN"])
            wire_stories.append({
                "headline":   random.choice(story_titles),
                "source":     random.choice(WIRE_SOURCES),
                "priority":   priority,
                "category":   random.choice(STORY_CATEGORIES),
                "received_at": (now - timedelta(minutes=random.randint(1, 60))).isoformat(),
                "word_count": random.randint(150, 800),
                "assigned":   random.choice([True, False]),
            })

        # Compute stats
        ready_count = sum(1 for i in rundown_items if i["status"] in ("ready", "on_air"))
        total_duration_min = sum(int(i["duration"].split(":")[0]) for i in rundown_items)

        return self.create_response(
            success=True,
            data={
                "show":             show_name,
                "system":           system,
                "rundown_items":    rundown_items,
                "total_items":      len(rundown_items),
                "ready_items":      ready_count,
                "total_duration":   f"{total_duration_min // 60}h {total_duration_min % 60}m",
                "wire_stories":     wire_stories,
                "urgent_wires":     sum(1 for w in wire_stories if w["priority"] == "URGENT"),
                "breaking_news":    any(w["priority"] == "URGENT" for w in wire_stories),
                "last_sync":        now.isoformat(),
                "mos_connection":   "active",
                "show_start":       now.replace(hour=18, minute=0).strftime("%H:%M"),
                "show_end":         now.replace(hour=18, minute=30).strftime("%H:%M"),
            },
            metadata={"mode": "demo", "newsroom_system": system},
        )

    async def _production_process(self, input_data: Any) -> Dict[str, Any]:
        inews_url = getattr(self.settings, "INEWS_API_URL", None)
        if not inews_url:
            raise ProductionNotReadyError(self.name, "INEWS_API_URL (or ENPS_API_URL)")

        try:
            import httpx
            mode = input_data.get("mode", "get_rundown") if isinstance(input_data, dict) else "get_rundown"
            show = input_data.get("show", "") if isinstance(input_data, dict) else ""

            async with httpx.AsyncClient(timeout=15) as client:
                if mode == "get_rundown":
                    endpoint = f"{inews_url}/shows/{show}/rundown" if show else f"{inews_url}/rundown/current"
                    resp = await client.get(endpoint)
                    resp.raise_for_status()
                    data = resp.json()
                elif mode == "sync":
                    endpoint = f"{inews_url}/sync"
                    resp = await client.post(endpoint, json=input_data)
                    resp.raise_for_status()
                    data = resp.json()
                else:
                    data = {}

            return self.create_response(
                success=True,
                data={
                    "rundown_items": data.get("items", []),
                    "total_items":   len(data.get("items", [])),
                    "last_sync":     datetime.now().isoformat(),
                    "mos_connection": "active",
                },
                metadata={"mode": "production", "newsroom_system": "iNews"},
            )
        except Exception as e:
            logger.error(f"Newsroom integration error: {e}", exc_info=True)
            return self.create_response(success=False, error=str(e))
