# alembic/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

# Це імпортує ваші моделі
from app.models import Base
from app.core.config import settings

# Зчитуємо конфігурацію з alembic.ini
config = context.config

# Оновлюємо конфігурацію бази даних
config.set_main_option('sqlalchemy.url', settings.DB_URL)

# Встановлюємо конфігурацію логування
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

async def run_migrations_online():
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    raise Exception("Offline mode is not supported with async")
else:
    import asyncio
    asyncio.run(run_migrations_online())
