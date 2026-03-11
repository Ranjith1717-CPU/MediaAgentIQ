"""
Operations endpoints — cancel, DLQ replay, DLQ list.

POST /ops/cancel/{task_id}   — cancel a queued or running task
POST /ops/replay/{dlq_id}    — re-submit a dead-lettered task
GET  /ops/dlq                — list dead-letter entries
GET  /ops/health             — (delegated to health.py router)
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from db import get_session_factory
from repositories import TaskRepository, DLQRepository
from queue.broker import get_redis, CANCEL_SET
from queue.tasks import enqueue_task_to_redis

logger = logging.getLogger("runtime.ops")

router = APIRouter(prefix="/ops", tags=["ops"])


@router.post("/cancel/{task_id}")
async def cancel_task(task_id: str) -> Dict[str, Any]:
    """
    Cancel a task.
    - Adds task_id to the Redis cancel set (worker checks before executing).
    - Updates status to CANCELLED in DB if the task is still QUEUED.
    """
    # Add to cancel set in Redis (TTL 1 hour — worker discards stale entries)
    try:
        client = get_redis()
        await client.sadd(CANCEL_SET, task_id)
        await client.expire(CANCEL_SET, 3600)
    except Exception as exc:
        logger.warning(f"Redis cancel-set write failed: {exc}")

    factory = get_session_factory()
    async with factory() as session:
        repo = TaskRepository(session)
        cancelled = await repo.cancel_task(task_id)

    return {"task_id": task_id, "cancelled": cancelled}


@router.post("/replay/{dlq_id}")
async def replay_dead_letter(dlq_id: int) -> Dict[str, Any]:
    """
    Re-submit a dead-lettered task.
    Creates a new task row with the same agent_key + input_data and enqueues it.
    """
    factory = get_session_factory()

    # Fetch DLQ entry
    async with factory() as session:
        dlq_repo = DLQRepository(session)
        entry = await dlq_repo.get_dead_letter(dlq_id)

    if entry is None:
        raise HTTPException(status_code=404, detail=f"DLQ entry {dlq_id} not found")
    if entry["replayed"]:
        raise HTTPException(status_code=409, detail=f"DLQ entry {dlq_id} already replayed")

    # Create new task
    async with factory() as session:
        task_repo = TaskRepository(session)
        new_task = await task_repo.create_task(
            agent_key=entry["agent_key"],
            input_data=entry["input_data"] or {},
            priority="NORMAL",
        )

    await enqueue_task_to_redis(new_task.id, "NORMAL")

    # Mark original DLQ entry as replayed
    async with factory() as session:
        dlq_repo = DLQRepository(session)
        await dlq_repo.mark_replayed(dlq_id)

    return {
        "replayed": True,
        "dlq_id": dlq_id,
        "new_task_id": new_task.id,
    }


@router.get("/dlq")
async def list_dlq(limit: int = 50) -> List[Dict[str, Any]]:
    """List dead-letter queue entries (most recent first)."""
    factory = get_session_factory()
    async with factory() as session:
        dlq_repo = DLQRepository(session)
        return await dlq_repo.list_dead_letters(limit=limit)
