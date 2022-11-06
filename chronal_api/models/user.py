from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

from chronal_api.db.chronal_psql import Base
from chronal_api.models import Timestamps


class User(SQLAlchemyBaseUserTableUUID, Timestamps, Base):
    first_name: str = Column(String(255), nullable=False)
    last_name: str = Column(String(255), nullable=False)
    timezone: str = Column(String(64), nullable=False)  # default: "Etc/UTC"
