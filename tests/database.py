from contextlib import contextmanager

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from chronal_api.settings import DatabaseSettings

db_settings = DatabaseSettings()

Session = scoped_session(sessionmaker(class_=AsyncSession, expire_on_commit=False))


@contextmanager
def init_test_database():
    db_sync_url = db_settings.get_url(async_=False).render_as_string()

    if database_exists(db_sync_url):
        drop_database(db_sync_url)

    create_database(db_sync_url)

    try:
        yield
    finally:
        drop_database(db_sync_url)
