from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from chronal_api.settings import DatabaseSettings

DB_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

db_settings = DatabaseSettings()
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)  # pyright: ignore


class Base(AsyncAttrs, DeclarativeBase):
    metadata = metadata


engine = create_async_engine(db_settings.get_url().render_as_string(), echo=True)

sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
