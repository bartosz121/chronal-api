import asyncio
from typing import AsyncIterator

import httpx
import pytest
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: F401
from sqlalchemy.ext.asyncio import async_scoped_session  # noqa: F401
from sqlalchemy.ext.asyncio import create_async_engine  # noqa: F401

from chronal_api.main import app
from chronal_api.settings import DatabaseSettings  # noqa: F401
from chronal_api.settings import get_app_settings

db_settings = get_app_settings()


@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(
        app=app,
        base_url="http://testserver",
    ) as client:
        yield client
