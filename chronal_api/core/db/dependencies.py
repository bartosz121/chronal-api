import logging

from sqlalchemy.ext.asyncio import AsyncSession

from chronal_api.core.db import async_session_maker
from chronal_api.core.debug import request_uuid_ctx

logger = logging.getLogger()


async def get_db_session():
    async with async_session_maker() as session:  # type: ignore https://github.com/dropbox/sqlalchemy-stubs/pull/231
        session: AsyncSession
        req_id = request_uuid_ctx.get()
        logger.debug("[%s] Opening session '%s'", req_id, id(session))
        try:
            yield session
        except Exception:
            await session.rollback()
        else:
            await session.commit()
        logger.debug("[%s] Closing session '%s'", req_id, id(session))
