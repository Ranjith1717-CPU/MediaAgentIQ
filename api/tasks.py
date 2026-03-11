"""
Task submission and status endpoints.

POST /api/tasks/submit  — create DB row + enqueue to Redis
GET  /api/tasks/{task_id} — poll task status
"""

from __future__ import annotations

import uuid
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from db import get_session_factory
from repositories import TaskRepository
from queue.tasks import enqueue_task_to_redis
from queue.dispatcher import list_registered_agents

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------

class TaskSubmitRequest(BaseModel):
    agent_key: str = Field(..., description="Agent identifier, e.g. 'compliance'")
    input_data: Dict[str, Any] = Field(default_factory=dict, description="Agent-specific input payload")
    priority: str = Field(default="NORMAL", description="CRITICAL | HIGH | NORMAL | LOW")


class TaskSubmitResponse(BaseModel):
    task_id: str
    status: str
    agent_key: str
    priority: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.post("/submit", response_model=TaskSubmitResponse, status_code=201)
async def submit_task(body: TaskSubmitRequest) -> TaskSubmitResponse:
    """Submit a new task to the runtime queue."""
    valid_agents = list_registered_agents()
    if body.agent_key not in valid_agents:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown agent_key '{body.agent_key}'. Valid: {valid_agents}",
        )

    valid_priorities = {"CRITICAL", "HIGH", "NORMAL", "LOW"}
    priority = body.priority.upper()
    if priority not in valid_priorities:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid priority '{body.priority}'. Valid: {sorted(valid_priorities)}",
        )

    task_id = str(uuid.uuid4())
    factory = get_session_factory()

    async with factory() as session:
        repo = TaskRepository(session)
        await repo.create_task(
            agent_key=body.agent_key,
            input_data=body.input_data,
            priority=priority,
            task_id=task_id,
        )

    await enqueue_task_to_redis(task_id, priority)

    return TaskSubmitResponse(
        task_id=task_id,
        status="QUEUED",
        agent_key=body.agent_key,
        priority=priority,
    )


@router.get("/{task_id}")
async def get_task_status(task_id: str) -> Dict[str, Any]:
    """Poll the status of a submitted task."""
    factory = get_session_factory()
    async with factory() as session:
        repo = TaskRepository(session)
        task = await repo.get_task_dict(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")

    return task
