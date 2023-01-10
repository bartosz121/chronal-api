from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import TIMESTAMP, Column, String, func
from sqlalchemy.orm import relationship

from chronal_api.core.db import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    first_name = Column[str](String(255), nullable=False)
    last_name = Column[str](String(255), nullable=False)
    timezone = Column[str](
        String(64), nullable=False, default="Etc/UTC"
    )  # TODO store timezones in db
    created_at = Column[datetime](
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column[datetime](
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    calendars = relationship("Calendar", back_populates="owner", cascade="all, delete")
    created_events = relationship("Event", back_populates="author")
    accesses = relationship(
        "CalendarAccess",
        back_populates="user",
        passive_deletes=True,
        foreign_keys="CalendarAccess.user_id",
    )
