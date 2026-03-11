"""
Redis broker — shared client and queue key definitions.
"""

from __future__ import annotations

import logging
from typing import Optional

import redis.asyncio as aioredis

from settings import settings

logger = logging.getLogger("runtime.broker")

# Priority → Redis list key (worker pops from highest priority first)
TASK_QUEUES: dict[str, str] = {
    "CRITICAL": "miq:queue:critical",
    "HIGH":     "miq:queue:high",
    "NORMAL":   "miq:queue:normal",
    "LOW":      "miq:queue:low",
}

# Set of cancelled task IDs (worker checks before executing)
CANCEL_SET = "miq:cancelled_tasks"

# Pub/sub channel prefix for per-task events
EVENT_CHANNEL_PREFIX = "miq:events:"
BROADCAST_CHANNEL = "miq:events:broadcast"

_redis_client: Optional[aioredis.Redis] = None


def get_redis() -> aioredis.Redis:
    """Return (or lazily create) the shared async Redis client."""
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )
    return _redis_client


async def ping_redis() -> bool:
    """Return True if Redis is reachable."""
    try:
        client = get_redis()
        await client.ping()
        return True
    except Exception as exc:
        logger.warning(f"Redis ping failed: {exc}")
        return False
