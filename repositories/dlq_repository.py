"""
DLQRepository — dead-letter queue operations.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db import DeadLetterModel


class DLQRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_dead_letter(
        self,
        task_id: str,
        agent_key: str,
        input_data: Dict[str, Any] | None,
        error_message: str,
        retries: int,
    ) -> DeadLetterModel:
        entry = DeadLetterModel(
            task_id=task_id,
            agent_key=agent_key,
            input_data=json.dumps(input_data) if input_data is not None else None,
            error_message=error_message,
            retries=retries,
            replayed=False,
        )
        self._session.add(entry)
        await self._session.commit()
        await self._session.refresh(entry)
        return entry

    async def get_dead_letter(self, dlq_id: int) -> Optional[Dict[str, Any]]:
        result = await self._session.execute(
            select(DeadLetterModel).where(DeadLetterModel.id == dlq_id)
        )
        row = result.scalar_one_or_none()
        return self._to_dict(row) if row else None

    async def list_dead_letters(self, limit: int = 50) -> List[Dict[str, Any]]:
        result = await self._session.execute(
            select(DeadLetterModel)
            .order_by(DeadLetterModel.created_at.desc())
            .limit(limit)
        )
        return [self._to_dict(r) for r in result.scalars().all()]

    async def mark_replayed(self, dlq_id: int) -> bool:
        result = await self._session.execute(
            update(DeadLetterModel)
            .where(DeadLetterModel.id == dlq_id, DeadLetterModel.replayed == False)  # noqa: E712
            .values(replayed=True, replayed_at=datetime.utcnow())
        )
        await self._session.commit()
        return result.rowcount > 0

    # ------------------------------------------------------------------

    @staticmethod
    def _to_dict(row: DeadLetterModel) -> Dict[str, Any]:
        return {
            "id": row.id,
            "task_id": row.task_id,
            "agent_key": row.agent_key,
            "input_data": json.loads(row.input_data) if row.input_data else None,
            "error_message": row.error_message,
            "retries": row.retries,
            "replayed": row.replayed,
            "replayed_at": row.replayed_at.isoformat() if row.replayed_at else None,
            "created_at": row.created_at.isoformat() if row.created_at else None,
        }
