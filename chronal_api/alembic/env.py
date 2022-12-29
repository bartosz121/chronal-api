from alembic import context
from sqlalchemy import create_engine

from chronal_api.auth.models import User
from chronal_api.calendar.models import Calendar
from chronal_api.calendar_access.models import CalendarAccess, CalendarAccessRole
from chronal_api.core.config import get_config
from chronal_api.core.db import Base

config = get_config()

engine = create_engine(config.postgres_uri_psycopg2)

with engine.connect() as connection:
    context.configure(connection, target_metadata=Base.metadata)

    with context.begin_transaction():
        context.run_migrations()
