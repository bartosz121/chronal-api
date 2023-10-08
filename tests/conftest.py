import asyncio
from typing import AsyncIterator, cast

import httpx
import pysqlite3
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from chronal_api.calendars import repository as calendars_repository
from chronal_api.calendars import service as calendars_service
from chronal_api.lib.auth import models as auth_models
from chronal_api.lib.database import dependencies as database_dependencies
from chronal_api.lib.database.engine import Base, metadata  # noqa: F401
from chronal_api.main import app
from chronal_api.settings import DatabaseSettings, get_app_settings
from tests import factories
from tests.database import Session, init_test_database

db_settings = DatabaseSettings()
app_settings = get_app_settings()


@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
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


@pytest.fixture(scope="function")
async def client(session) -> AsyncIterator[httpx.AsyncClient]:
    assert app_settings.ENVIRONMENT == "TESTING"

    app.dependency_overrides[database_dependencies.db_session] = lambda: session

    async with httpx.AsyncClient(
        app=app,
        base_url="http://testserver",
    ) as client:
        yield client


@pytest.fixture(scope="function")
async def authorized_client(
    client: httpx.AsyncClient,
) -> AsyncIterator[tuple[httpx.AsyncClient, auth_models.AccessToken]]:
    token = await factories.AccessTokenFactory.create()
    client.headers.update({"Authorization": f"Bearer {token.access_token}"})
    yield client, token


@pytest.fixture
def user_factory() -> type[factories.UserFactory]:
    return factories.UserFactory


@pytest.fixture
def access_token_factory() -> type[factories.AccessTokenFactory]:
    return factories.AccessTokenFactory


@pytest.fixture
def calendar_factory() -> type[factories.CalendarFactory]:
    return factories.CalendarFactory


@pytest.fixture
def calendar_repository(session: AsyncSession) -> calendars_repository.CalendarRepository:
    return calendars_repository.CalendarRepository(session)


@pytest.fixture
def calendar_service(
    calendar_repository: calendars_repository.CalendarRepository,
) -> calendars_service.CalendarService:
    return calendars_service.CalendarService(calendar_repository)
