import logging
import uuid
from datetime import datetime

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, event, func, insert
from sqlalchemy.orm import relationship

from chronal_api.calendar_access.models import CalendarAccess, CalendarAccessRole
from chronal_api.core.db import Base

# TODO repr


logger = logging.getLogger()


class Calendar(Base):
    __tablename__ = "calendars"
    id = Column[uuid.UUID](GUID, primary_key=True, default=uuid.uuid4)
    name = Column[str](String(255), nullable=False)
    description = Column[str](String(255), nullable=True)
    owner_id = Column[uuid.UUID](GUID, ForeignKey("users.id", ondelete="CASCADE"))
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

    owner = relationship("User", back_populates="calendars")
    events = relationship(
        "Event",
        back_populates="calendar",
        passive_deletes=True,
    )
    access_list = relationship(
        "CalendarAccess", back_populates="calendar", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"Calendar #{self.id}"


@event.listens_for(Calendar, "after_insert")
def create_calendar_access_for_owner(mapper, connection, target: Calendar):
    connection.execute(
        insert(CalendarAccess).values(
            calendar_id=target.id,
            user_id=target.owner_id,
            role=CalendarAccessRole.OWNER.value,
            created_by=target.owner_id,
        )
    )
