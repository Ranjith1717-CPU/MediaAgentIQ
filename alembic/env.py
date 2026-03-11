"""
Alembic async-compatible env.py for MediaAgentIQ runtime layer.
Supports both SQLite (dev) and PostgreSQL (production).
"""

from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

# Alembic Config object — provides access to alembic.ini values
config = context.config

# Set up Python logging from alembic.ini if present
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import the ORM metadata so Alembic can detect table changes
from db import Base  # noqa: E402
target_metadata = Base.metadata


def get_url() -> str:
    """Get the database URL from settings (respects env vars)."""
    from settings import settings
    return settings.RUNTIME_DATABASE_URL


# ---------------------------------------------------------------------------
# Offline mode (generate SQL without connecting to DB)
# ---------------------------------------------------------------------------

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,  # required for SQLite ALTER TABLE
    )
    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------------------------
# Online mode (connect to DB and run migrations)
# ---------------------------------------------------------------------------

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,  # required for SQLite ALTER TABLE
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = create_async_engine(get_url(), echo=False)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
