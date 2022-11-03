from alembic import context
from sqlalchemy import create_engine


from chronal_api.core.config import get_config
from chronal_api.db import chronal_psql

config = get_config()

engine = create_engine(config.postgres_uri_psycopg2)

with engine.connect() as connection:
    context.configure(connection, target_metadata=chronal_psql.Base.metadata)

    with context.begin_transaction():
        context.run_migrations()
