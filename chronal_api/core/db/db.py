from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from chronal_api.core.config import get_config

config = get_config()

Base = declarative_base()


engine = create_async_engine(
    config.postgres_uri,
    future=True,
    echo=config.IS_DEV,
)

async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
