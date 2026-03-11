"""
TaskRepository — CRUD operations for TaskModel.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db import TaskModel
from settings import settings


class TaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    async def create_task(
        self,
        agent_key: str,
        input_data: Dict[str, Any],
        priority: str = "NORMAL",
        task_id: Optional[str] = None,
    ) -> TaskModel:
        task = TaskModel(
            id=task_id or str(uuid.uuid4()),
            agent_key=agent_key,
            priority=priority,
            status="QUEUED",
            input_data=json.dumps(input_data),
            max_retries=settings.TASK_MAX_RETRIES,
        )
        self._session.add(task)
        await self._session.commit()
        await self._session.refresh(task)
        return task

    async def mark_running(self, task_id: str, worker_id: str) -> bool:
        result = await self._session.execute(
            update(TaskModel)
            .where(TaskModel.id == task_id, TaskModel.status == "QUEUED")
            .values(status="RUNNING", worker_id=worker_id, started_at=datetime.utcnow())
        )
        await self._session.commit()
        return result.rowcount > 0

    async def mark_completed(self, task_id: str, output_data: Dict[str, Any]) -> None:
        await self._session.execute(
            update(TaskModel)
            .where(TaskModel.id == task_id)
            .values(
                status="COMPLETED",
                output_data=json.dumps(output_data),
                completed_at=datetime.utcnow(),
            )
        )
        await self._session.commit()

    async def mark_failed(self, task_id: str, error_message: str) -> None:
        await self._session.execute(
            update(TaskModel)
            .where(TaskModel.id == task_id)
            .values(
                status="FAILED",
                error_message=error_message,
                completed_at=datetime.utcnow(),
            )
        )
        await self._session.commit()

    async def cancel_task(self, task_id: str) -> bool:
        result = await self._session.execute(
            update(TaskModel)
            .where(TaskModel.id == task_id, TaskModel.status.in_(["QUEUED", "RUNNING"]))
            .values(status="CANCELLED")
        )
        await self._session.commit()
        return result.rowcount > 0

    async def increment_retry(self, task_id: str) -> Dict[str, int]:
        """Increment retry counter and return {retries, max_retries}."""
        task = await self.get_task(task_id)
        if task is None:
            return {"retries": 0, "max_retries": settings.TASK_MAX_RETRIES}
        new_retries = task.retries + 1
        await self._session.execute(
            update(TaskModel)
            .where(TaskModel.id == task_id)
            .values(retries=new_retries, status="QUEUED")
        )
        await self._session.commit()
        return {"retries": new_retries, "max_retries": task.max_retries}

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    async def get_task(self, task_id: str) -> Optional[TaskModel]:
        result = await self._session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        return result.scalar_one_or_none()

    async def get_task_dict(self, task_id: str) -> Optional[Dict[str, Any]]:
        task = await self.get_task(task_id)
        if task is None:
            return None
        return {
            "task_id": task.id,
            "agent_key": task.agent_key,
            "priority": task.priority,
            "status": task.status,
            "retries": task.retries,
            "max_retries": task.max_retries,
            "worker_id": task.worker_id,
            "error_message": task.error_message,
            "output_data": json.loads(task.output_data) if task.output_data else None,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        }
