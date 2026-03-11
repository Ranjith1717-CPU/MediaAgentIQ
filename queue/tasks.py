"""
Task enqueueing — pushes task IDs into Redis priority queues.
"""

from __future__ import annotations

import logging

from .broker import get_redis, TASK_QUEUES

logger = logging.getLogger("runtime.queue.tasks")

_DEFAULT_PRIORITY = "NORMAL"


async def enqueue_task_to_redis(task_id: str, priority: str = _DEFAULT_PRIORITY) -> None:
    """
    Push task_id onto the left of the appropriate priority queue list.
    Worker uses BRPOP (right-pop) so this is FIFO within a priority band.
    Falls back to NORMAL queue if priority is unrecognised.
    """
    queue_key = TASK_QUEUES.get(priority.upper(), TASK_QUEUES[_DEFAULT_PRIORITY])
    try:
        client = get_redis()
        await client.lpush(queue_key, task_id)
        logger.debug(f"Enqueued task {task_id} → {queue_key}")
    except Exception as exc:
        logger.error(f"Failed to enqueue task {task_id}: {exc}")
        raise
