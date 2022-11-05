import logging
from typing import Generator

from contextvars import ContextVar

from fastapi import HTTPException
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from chronal_api.core.config import get_config
from chronal_api.core.debug import REQUEST_UUID

config = get_config()

Base: DeclarativeMeta = declarative_base()

engine = create_async_engine(config.postgres_uri, future=True, echo=config.IS_DEV)
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

psql_session: ContextVar[AsyncSession] = ContextVar("psql_session")


async def get_psql_db() -> Generator[AsyncSession, None, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except Exception as exc:
            exc_str = exc
            if isinstance(exc, HTTPException):
                exc_str = exc.detail
            logging.error("[%s] %s %s", REQUEST_UUID.get(), session, exc_str)
            await session.rollback()
        else:
            await session.commit()
