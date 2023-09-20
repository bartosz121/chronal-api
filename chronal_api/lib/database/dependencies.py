from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .engine import sessionmaker


async def db_session() -> AsyncGenerator[AsyncSession, None]:
    session = sessionmaker()
    async with sessionmaker() as session:
        async with session.begin():
            yield session


# Annotated

DbSession = Annotated[AsyncSession, Depends(db_session)]
