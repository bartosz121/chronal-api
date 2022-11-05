from sqlalchemy import Column, String
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

from chronal_api.db import chronal_psql


class User(SQLAlchemyBaseUserTableUUID, chronal_psql.Base):
    first_name: str = Column(String(255), nullable=False)
    last_name: str = Column(String(255), nullable=False)
