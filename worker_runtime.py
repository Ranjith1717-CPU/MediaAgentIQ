"""
MediaAgentIQ Runtime Worker
===========================
Pulls task IDs from Redis priority queues (BRPOP), executes the correct agent,
persists results to the runtime DB, publishes SSE events, and handles retries /
dead-letter routing.

Run:
    python worker_runtime.py

The worker is safe to run alongside the existing orchestrator.py — they use
different queues and the same agents (via singletons in dispatcher).
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import socket
import sys
import time
import uuid
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Logging setup (before any local imports so handler is ready)
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("runtime.worker")

# ---------------------------------------------------------------------------
# Local imports (after logging)
# ---------------------------------------------------------------------------
from settings import settings
from db import get_session_factory, TaskModel, WorkerHeartbeatModel
from repositories import TaskRepository, EventRepository, DLQRepository
from queue.broker import get_redis, TASK_QUEUES, CANCEL_SET
from queue.dispatcher import execute_agent_task
from queue.events import publish_event

# ---------------------------------------------------------------------------
# Worker identity
# ---------------------------------------------------------------------------
WORKER_ID: str = f"worker-{socket.gethostname()}-{os.getpid()}-{uuid.uuid4().hex[:6]}"

# Ordered list of queue keys — worker drains higher-priority queues first
PRIORITY_ORDER: List[str] = [
    TASK_QUEUES["CRITICAL"],
    TASK_QUEUES["HIGH"],
    TASK_QUEUES["NORMAL"],
    TASK_QUEUES["LOW"],
]

# ---------------------------------------------------------------------------
# Cancellation check
# ---------------------------------------------------------------------------

async def is_cancelled(task_id: str) -> bool:
    """Return True if the task has been added to the cancel set."""
    try:
        client = get_redis()
        return bool(await client.sismember(CANCEL_SET, task_id))
    except Exception as exc:
        logger.warning(f"Cancel check failed for {task_id}: {exc}")
        return False

# ---------------------------------------------------------------------------
# DB helpers — each uses its own short-lived session
# ---------------------------------------------------------------------------

async def load_task(task_id: str) -> Optional[Dict[str, Any]]:
    factory = get_session_factory()
    async with factory() as session:
        repo = TaskRepository(session)
        return await repo.get_task_dict(task_id)


async def claim_task(task_id: str) -> bool:
    """Transition task QUEUED → RUNNING. Returns False if already claimed."""
    factory = get_session_factory()
    async with factory() as session:
        repo = TaskRepository(session)
        return await repo.mark_running(task_id, WORKER_ID)


async def complete_task(task_id: str, output_data: Dict[str, Any]) -> None:
    factory = get_session_factory()
    async with factory() as session:
        repo = TaskRepository(session)
        await repo.mark_completed(task_id, output_data)
    await _add_event(task_id, "completed", {"output": output_data})
    await publish_event(task_id, "completed", {"output": output_data})


async def fail_or_retry_task(task_id: str, error_message: str) -> None:
    """
    Increment retry counter.
    - If retries < max_retries: re-enqueue with backoff.
    - Otherwise: mark FAILED and move to DLQ.
    """
    # --- path 1: increment + read counters ---
    factory = get_session_factory()
    async with factory() as session:
        repo = TaskRepository(session)
        counts = await repo.increment_retry(task_id)
        retries = counts["retries"]
        max_retries = counts["max_retries"]

    if retries < max_retries:
        backoff = settings.TASK_RETRY_BACKOFF_SECONDS * retries
        logger.info(
            f"Task {task_id} retry {retries}/{max_retries} — backoff {backoff}s"
        )
        await _add_event(task_id, "retry", {"retries": retries, "backoff_secs": backoff})
        await publish_event(task_id, "retry", {"retries": retries})
        await asyncio.sleep(backoff)

        # Re-enqueue (use same priority stored on the task)
        task_dict = await load_task(task_id)
        priority = task_dict["priority"] if task_dict else "NORMAL"
        from queue.tasks import enqueue_task_to_redis
        await enqueue_task_to_redis(task_id, priority)
    else:
        # --- path 2: mark FAILED + send to DLQ ---
        async with factory() as session:
            task_repo = TaskRepository(session)
            await task_repo.mark_failed(task_id, error_message)

        # Write DLQ entry in a fresh session
        task_dict = await load_task(task_id)
        async with factory() as session:
            dlq_repo = DLQRepository(session)
            await dlq_repo.add_dead_letter(
                task_id=task_id,
                agent_key=task_dict["agent_key"] if task_dict else "unknown",
                input_data=None,
                error_message=error_message,
                retries=retries,
            )

        await _add_event(task_id, "dead_lettered", {"error": error_message})
        await publish_event(task_id, "failed", {"error": error_message})
        logger.error(
            f"Task {task_id} permanently failed after {retries} retries → DLQ"
        )


async def _add_event(task_id: str, event_type: str, payload: Dict[str, Any]) -> None:
    factory = get_session_factory()
    async with factory() as session:
        repo = EventRepository(session)
        await repo.add_event(task_id, event_type, payload)

# ---------------------------------------------------------------------------
# Heartbeat
# ---------------------------------------------------------------------------

async def _write_heartbeat(current_task_id: Optional[str] = None) -> None:
    factory = get_session_factory()
    try:
        async with factory() as session:
            existing = await session.get(WorkerHeartbeatModel, WORKER_ID)
            if existing is None:
                hb = WorkerHeartbeatModel(
                    worker_id=WORKER_ID,
                    tasks_processed=0,
                    current_task_id=current_task_id,
                    status="running" if current_task_id else "idle",
                )
                session.add(hb)
            else:
                from datetime import datetime
                existing.last_seen = datetime.utcnow()
                existing.current_task_id = current_task_id
                existing.status = "running" if current_task_id else "idle"
            await session.commit()
    except Exception as exc:
        logger.warning(f"Heartbeat write failed: {exc}")


async def heartbeat_loop() -> None:
    """Background coroutine that writes a heartbeat every N seconds."""
    while True:
        await _write_heartbeat()
        await asyncio.sleep(settings.WORKER_HEARTBEAT_INTERVAL_SECS)

# ---------------------------------------------------------------------------
# Core task processor
# ---------------------------------------------------------------------------

async def process_task_id(task_id: str) -> None:
    """End-to-end processing of a single task ID."""
    logger.info(f"Picked up task {task_id}")

    # 1. Cancel check
    if await is_cancelled(task_id):
        logger.info(f"Task {task_id} is cancelled — skipping")
        async with get_session_factory()() as session:
            await TaskRepository(session).cancel_task(task_id)
        await publish_event(task_id, "cancelled", {})
        return

    # 2. Load + claim
    task_dict = await load_task(task_id)
    if task_dict is None:
        logger.warning(f"Task {task_id} not found in DB — ignoring")
        return

    claimed = await claim_task(task_id)
    if not claimed:
        logger.warning(f"Task {task_id} already claimed by another worker — skipping")
        return

    await _add_event(task_id, "running", {"worker_id": WORKER_ID})
    await publish_event(task_id, "running", {"worker_id": WORKER_ID})

    # 3. Determine per-agent timeout
    agent_key = task_dict["agent_key"]
    try:
        timeout_map: Dict[str, int] = json.loads(settings.AGENT_TIMEOUT_JSON)
    except Exception:
        timeout_map = {}
    timeout_secs = timeout_map.get(agent_key, settings.API_TIMEOUT_SECONDS)

    # 4. Execute
    try:
        input_data = (
            json.loads(task_dict.get("input_data") or "{}")
            if isinstance(task_dict.get("input_data"), str)
            else task_dict.get("input_data") or {}
        )
        result = await asyncio.wait_for(
            execute_agent_task(agent_key, input_data),
            timeout=timeout_secs,
        )
        if result.get("success", True):
            await complete_task(task_id, result)
        else:
            error = result.get("error") or "Agent returned success=False"
            await fail_or_retry_task(task_id, error)
    except asyncio.TimeoutError:
        await fail_or_retry_task(task_id, f"Timeout after {timeout_secs}s")
    except Exception as exc:
        await fail_or_retry_task(task_id, str(exc))

# ---------------------------------------------------------------------------
# Queue poller
# ---------------------------------------------------------------------------

async def pop_next_task_id() -> Optional[str]:
    """
    BRPOP across all priority queues (highest priority first).
    Blocks for WORKER_QUEUE_POLL_TIMEOUT_SECS seconds.
    Returns task_id string or None on timeout.
    """
    client = get_redis()
    try:
        item = await client.brpop(PRIORITY_ORDER, timeout=settings.WORKER_QUEUE_POLL_TIMEOUT_SECS)
        if item:
            _queue_key, task_id = item
            return task_id
    except Exception as exc:
        logger.warning(f"BRPOP error: {exc}")
        await asyncio.sleep(2)
    return None

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

async def run_forever() -> None:
    logger.info(f"Worker {WORKER_ID} starting — concurrency={settings.WORKER_CONCURRENCY}")
    semaphore = asyncio.Semaphore(settings.WORKER_CONCURRENCY)

    asyncio.create_task(heartbeat_loop())

    while True:
        task_id = await pop_next_task_id()
        if task_id is None:
            continue

        async def _run(tid: str) -> None:
            async with semaphore:
                try:
                    await process_task_id(tid)
                except Exception as exc:
                    logger.exception(f"Unhandled error processing task {tid}: {exc}")

        asyncio.create_task(_run(task_id))


if __name__ == "__main__":
    asyncio.run(run_forever())
