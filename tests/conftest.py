import asyncio
import logging

import httpx
import pytest
import pytest_asyncio
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from chronal_api.auth.models import User
from chronal_api.core import db as core_db
from chronal_api.core.config import TestConfig
from chronal_api.core.db.dependencies import get_db_session
from chronal_api.main import app

from .data import (
    AUTH_CLIENT_SUPERUSER,
    AUTH_CLIENT_USER0,
    AUTH_CLIENT_USER1,
    AUTH_CLIENT_USER2,
    AUTH_CLIENT_USER3,
    AUTH_CLIENT_USER4,
    AUTH_CLIENT_USER5,
    add_data,
    user_password,
)

test_config = TestConfig()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(test_config.test_postgres_uri, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(core_db.Base.metadata.drop_all)  # TODO remove this later

    async with engine.begin() as conn:
        await conn.run_sync(core_db.Base.metadata.create_all)

    await add_data(engine)

    try:
        yield engine
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(core_db.Base.metadata.drop_all)

    engine.sync_engine.dispose()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def session(engine: AsyncEngine):
    connection = await engine.connect()
    await connection.begin()
    db = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )()

    logging.info("YIELDING DB")
    yield db
    # TODO this
    logging.info("ROLLINGBACK DB")
    await db.rollback()
    await connection.close()


@pytest_asyncio.fixture(scope="function")
async def client(session: AsyncSession) -> httpx.AsyncClient:
    app.dependency_overrides[get_db_session] = lambda: session

    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
async def user_db(session):
    yield SQLAlchemyUserDatabase(session, User)


async def get_access_token(client_: httpx.AsyncClient, data: dict) -> str:
    response = await client_.post(
        "/api/v1/auth/jwt/login",
        data=data,
    )

    if response.status_code != 200:
        raise Exception(f"get_access_token response != 200; {vars(response)}")

    return response.json()["access_token"]


@pytest_asyncio.fixture
async def user0_client(client: httpx.AsyncClient):
    access_token = await get_access_token(
        client,
        {
            "username": AUTH_CLIENT_USER0["email"],
            "password": user_password,
        },
    )
    client.headers["Authorization"] = f"Bearer {access_token}"
    yield client


@pytest_asyncio.fixture
async def user1_client(client: httpx.AsyncClient):
    access_token = await get_access_token(
        client,
        {
            "username": AUTH_CLIENT_USER1["email"],
            "password": user_password,
        },
    )
    client.headers["Authorization"] = f"Bearer {access_token}"
    yield client


@pytest_asyncio.fixture
async def user2_client(client: httpx.AsyncClient):
    access_token = await get_access_token(
        client,
        {
            "username": AUTH_CLIENT_USER2["email"],
            "password": user_password,
        },
    )
    client.headers["Authorization"] = f"Bearer {access_token}"
    yield client


@pytest_asyncio.fixture
async def user3_client(client: httpx.AsyncClient):
    access_token = await get_access_token(
        client,
        {
            "username": AUTH_CLIENT_USER3["email"],
            "password": user_password,
        },
    )
    client.headers["Authorization"] = f"Bearer {access_token}"
    yield client


@pytest_asyncio.fixture
async def user4_client(client: httpx.AsyncClient):
    access_token = await get_access_token(
        client,
        {
            "username": AUTH_CLIENT_USER4["email"],
            "password": user_password,
        },
    )
    client.headers["Authorization"] = f"Bearer {access_token}"
    yield client


@pytest_asyncio.fixture
async def user5_client(client: httpx.AsyncClient):
    access_token = await get_access_token(
        client,
        {
            "username": AUTH_CLIENT_USER5["email"],
            "password": user_password,
        },
    )
    client.headers["Authorization"] = f"Bearer {access_token}"
    yield client


@pytest_asyncio.fixture
async def superuser_client(client: httpx.AsyncClient):
    access_token = await get_access_token(
        client,
        {
            "username": AUTH_CLIENT_SUPERUSER["email"],
            "password": user_password,
        },
    )
    client.headers["Authorization"] = f"Bearer {access_token}"
    yield client
