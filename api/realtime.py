"""
Server-Sent Events (SSE) endpoint for real-time task updates.

GET /api/realtime/events?task_id=<uuid>   — stream events for a specific task
GET /api/realtime/events                  — stream all broadcast events
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import AsyncGenerator, Optional

from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

from queue.broker import get_redis, EVENT_CHANNEL_PREFIX, BROADCAST_CHANNEL
from settings import settings

logger = logging.getLogger("runtime.realtime")

router = APIRouter(prefix="/api/realtime", tags=["realtime"])


async def _event_generator(task_id: Optional[str]) -> AsyncGenerator[dict, None]:
    """
    Subscribe to Redis pub/sub for task events.
    Yields SSE-compatible dicts with 'data' key.
    Sends keepalive comments every RUNTIME_SSE_KEEPALIVE_SECS seconds.
    """
    client = get_redis()
    pubsub = client.pubsub()

    channel = (
        f"{EVENT_CHANNEL_PREFIX}{task_id}" if task_id else BROADCAST_CHANNEL
    )

    await pubsub.subscribe(channel)
    logger.info(f"SSE subscriber connected — channel: {channel}")

    try:
        last_keepalive = asyncio.get_event_loop().time()
        while True:
            now = asyncio.get_event_loop().time()

            # Send keepalive comment if idle
            if now - last_keepalive >= settings.RUNTIME_SSE_KEEPALIVE_SECS:
                yield {"comment": "keepalive"}
                last_keepalive = now

            message = await pubsub.get_message(
                ignore_subscribe_messages=True, timeout=1.0
            )
            if message and message.get("type") == "message":
                raw = message.get("data", "{}")
                try:
                    payload = json.loads(raw)
                except json.JSONDecodeError:
                    payload = {"raw": raw}
                yield {"data": json.dumps(payload)}

                # Auto-close stream once task reaches terminal state
                event_type = payload.get("event", "")
                if task_id and event_type in ("completed", "failed", "cancelled"):
                    break

            await asyncio.sleep(0.05)

    except asyncio.CancelledError:
        pass
    finally:
        await pubsub.unsubscribe(channel)
        logger.info(f"SSE subscriber disconnected — channel: {channel}")


@router.get("/events")
async def stream_events(task_id: Optional[str] = None) -> EventSourceResponse:
    """
    Stream task events via SSE.
    - Pass ?task_id=<uuid> to subscribe to a specific task.
    - Omit task_id to receive all broadcast events.
    """
    return EventSourceResponse(_event_generator(task_id))
