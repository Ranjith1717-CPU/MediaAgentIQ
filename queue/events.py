"""
Event publishing — pushes JSON events to per-task and broadcast pub/sub channels.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any, Dict

from .broker import get_redis, EVENT_CHANNEL_PREFIX, BROADCAST_CHANNEL

logger = logging.getLogger("runtime.events")


async def publish_event(
    task_id: str,
    event_type: str,
    payload: Dict[str, Any] | None = None,
) -> None:
    """
    Publish a task event to two Redis pub/sub channels:
      - miq:events:{task_id}  — per-task SSE stream
      - miq:events:broadcast   — fan-out to all connected SSE clients
    """
    message = json.dumps(
        {
            "task_id": task_id,
            "event": event_type,
            "payload": payload or {},
            "ts": datetime.utcnow().isoformat(),
        }
    )
    try:
        client = get_redis()
        per_task_channel = f"{EVENT_CHANNEL_PREFIX}{task_id}"
        await client.publish(per_task_channel, message)
        await client.publish(BROADCAST_CHANNEL, message)
    except Exception as exc:
        logger.warning(f"publish_event failed for task {task_id}: {exc}")
