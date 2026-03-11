"""Create runtime tables: tasks, task_events, dead_letters, worker_heartbeats

Revision ID: 001
Revises:
Create Date: 2026-03-11 00:00:00.000000

"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------ tasks
    op.create_table(
        "tasks",
        sa.Column("id", sa.String(36), primary_key=True, nullable=False),
        sa.Column("agent_key", sa.String(64), nullable=False),
        sa.Column("priority", sa.String(16), nullable=False, server_default="NORMAL"),
        sa.Column("status", sa.String(16), nullable=False, server_default="QUEUED"),
        sa.Column("input_data", sa.Text, nullable=True),
        sa.Column("output_data", sa.Text, nullable=True),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("retries", sa.Integer, nullable=False, server_default="0"),
        sa.Column("max_retries", sa.Integer, nullable=False, server_default="3"),
        sa.Column("worker_id", sa.String(128), nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("started_at", sa.DateTime, nullable=True),
        sa.Column("completed_at", sa.DateTime, nullable=True),
    )
    op.create_index("ix_tasks_agent_key", "tasks", ["agent_key"])
    op.create_index("ix_tasks_status", "tasks", ["status"])
    op.create_index("ix_tasks_status_priority", "tasks", ["status", "priority"])

    # ------------------------------------------------------------ task_events
    op.create_table(
        "task_events",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("task_id", sa.String(36), nullable=False),
        sa.Column("event_type", sa.String(64), nullable=False),
        sa.Column("payload", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_task_events_task_id", "task_events", ["task_id"])

    # ------------------------------------------------------------ dead_letters
    op.create_table(
        "dead_letters",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("task_id", sa.String(36), nullable=False),
        sa.Column("agent_key", sa.String(64), nullable=False),
        sa.Column("input_data", sa.Text, nullable=True),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("retries", sa.Integer, nullable=False, server_default="0"),
        sa.Column("replayed", sa.Boolean, nullable=False, server_default="0"),
        sa.Column("replayed_at", sa.DateTime, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_dead_letters_task_id", "dead_letters", ["task_id"])

    # ------------------------------------------------------- worker_heartbeats
    op.create_table(
        "worker_heartbeats",
        sa.Column("worker_id", sa.String(128), primary_key=True, nullable=False),
        sa.Column("last_seen", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("tasks_processed", sa.Integer, nullable=False, server_default="0"),
        sa.Column("current_task_id", sa.String(36), nullable=True),
        sa.Column("status", sa.String(16), nullable=False, server_default="idle"),
    )


def downgrade() -> None:
    op.drop_table("worker_heartbeats")
    op.drop_table("dead_letters")
    op.drop_table("task_events")
    op.drop_table("tasks")
