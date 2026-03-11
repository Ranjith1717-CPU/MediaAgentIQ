"""
EventRepository — append-only task event log.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import TaskEventModel


class EventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_event(
        self,
        task_id: str,
        event_type: str,
        payload: Dict[str, Any] | None = None,
    ) -> TaskEventModel:
        event = TaskEventModel(
            task_id=task_id,
            event_type=event_type,
            payload=json.dumps(payload) if payload is not None else None,
        )
        self._session.add(event)
        await self._session.commit()
        await self._session.refresh(event)
        return event

    async def get_events(self, task_id: str) -> List[Dict[str, Any]]:
        result = await self._session.execute(
            select(TaskEventModel)
            .where(TaskEventModel.task_id == task_id)
            .order_by(TaskEventModel.created_at)
        )
        rows = result.scalars().all()
        return [
            {
                "id": r.id,
                "task_id": r.task_id,
                "event_type": r.event_type,
                "payload": json.loads(r.payload) if r.payload else None,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]
