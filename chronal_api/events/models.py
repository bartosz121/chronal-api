import uuid
from datetime import datetime

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import TIMESTAMP, Column, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CheckConstraint

from chronal_api.core.abc import UUID
from chronal_api.core.db import Base


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (CheckConstraint("start_dt < end_dt"),)
    id = Column[UUID](GUID, primary_key=True, default=uuid.uuid4)
    title = Column[str](String(255), nullable=False)
    description = Column[str](Text, nullable=True)
    start_dt = Column[datetime](TIMESTAMP(timezone=True), nullable=False)
    end_dt = Column[datetime](TIMESTAMP(timezone=True), nullable=False)
    timezone = Column[str](String(64), nullable=False, default="Etc/UTC")
    calendar_id = Column[UUID](
        GUID, ForeignKey("calendars.id", ondelete="CASCADE"), nullable=False
    )
    created_by = Column[UUID](
        GUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
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

    calendar = relationship(
        "Calendar",
        back_populates="events",
        cascade="all, delete",
    )
    author = relationship(
        "User",
        back_populates="created_events",
        cascade="all, delete",  # TODO not `all, delete` ??
    )
