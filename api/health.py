"""
Health check endpoint.

GET /ops/health  — returns DB + Redis status and live worker count.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from fastapi import APIRouter
from sqlalchemy import text, select, func

from db import get_session_factory, WorkerHeartbeatModel
from queue.broker import ping_redis

logger = logging.getLogger("runtime.health")

router = APIRouter(prefix="/ops", tags=["ops"])


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Liveness + readiness check for the runtime layer."""
    result: Dict[str, Any] = {}

    # Redis
    redis_ok = await ping_redis()
    result["redis"] = "ok" if redis_ok else "unreachable"

    # DB
    try:
        factory = get_session_factory()
        async with factory() as session:
            await session.execute(text("SELECT 1"))
        result["db"] = "ok"
    except Exception as exc:
        result["db"] = f"error: {exc}"

    # Live worker count (heartbeats seen in last 60 seconds)
    try:
        from datetime import datetime, timedelta
        cutoff = datetime.utcnow() - timedelta(seconds=60)
        factory = get_session_factory()
        async with factory() as session:
            count_result = await session.execute(
                select(func.count(WorkerHeartbeatModel.worker_id))
                .where(WorkerHeartbeatModel.last_seen >= cutoff)
            )
            worker_count = count_result.scalar_one_or_none() or 0
        result["worker_count"] = worker_count
    except Exception as exc:
        result["worker_count"] = f"error: {exc}"

    result["status"] = "healthy" if result["redis"] == "ok" and result["db"] == "ok" else "degraded"
    return result
