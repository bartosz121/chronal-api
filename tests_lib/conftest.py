import asyncio
from typing import AsyncIterator

import pysqlite3
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .models import Base, TodoItem

DUMMY_COUNT = 1000


async def insert_dummy(
    session: AsyncSession,
) -> None:
    from random import randint

    items = [
        TodoItem(title=f"Item {i}", description=f"{i}", is_complete=bool(randint(0, 1))) for i in range(DUMMY_COUNT)
    ]
    session.add_all(items)
    await session.commit()


@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        module=pysqlite3,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )

    async with async_session() as session:
        async with session.begin():
            await insert_dummy(async_session())

    session = async_session()
    await session.begin()

    yield session

    await session.close()
    await engine.dispose()
