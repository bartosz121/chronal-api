import asyncio
from typing import AsyncIterator, cast

import pysqlite3
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from chronal_api.settings import DatabaseSettings, get_app_settings
from tests.database import Session, init_test_database

from .models import Base, TodoItem

DUMMY_COUNT = 1000

db_settings = DatabaseSettings()
app_settings = get_app_settings()


@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def db():
    assert db_settings.NAME.endswith("test")

    with init_test_database():
        db_async_url = db_settings.get_url()
        engine = create_async_engine(db_async_url.render_as_string(), module=pysqlite3)

        async with engine.connect() as conn:
            await conn.run_sync(Base.metadata.create_all)

        Session.configure(bind=engine)

        yield


@pytest.fixture(scope="function")
async def session() -> AsyncIterator[AsyncSession]:
    session = cast(AsyncSession, Session())
    session.begin_nested()
    yield session
    await session.rollback()


@pytest.fixture()
async def insert_dummy(
    session: AsyncSession,
) -> None:
    from random import randint

    items = [
        TodoItem(title=f"Item {i}", description=f"{i}", is_completed=bool(randint(0, 1)))
        for i in range(DUMMY_COUNT)
    ]
    session.add_all(items)
    await session.commit()
