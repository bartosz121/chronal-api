from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from chronal_api.settings import DatabaseSettings

db_settings = DatabaseSettings()

engine = create_async_engine(db_settings.url, echo=db_settings.ECHO)

sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
