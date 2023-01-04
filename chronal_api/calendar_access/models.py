import uuid
from datetime import datetime
from enum import Enum

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import TIMESTAMP, Column
from sqlalchemy import Enum as SqlaEnum
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship

from chronal_api.core.abc import UUID
from chronal_api.core.db import Base


class CalendarAccessRole(str, Enum):
    OWNER = "OWNER"
    MODERATOR = "MODERATOR"
    STANDARD = "STANDARD"
    GUEST = "GUEST"


class CalendarAccess(Base):
    __tablename__ = "calendars_access"
    id = Column[UUID](GUID, primary_key=True, default=uuid.uuid4)
    calendar_id = Column[UUID](GUID, ForeignKey("calendars.id", ondelete="CASCADE"))
    user_id = Column[UUID](GUID, ForeignKey("users.id", ondelete="CASCADE"))
    role = Column[CalendarAccessRole](
        SqlaEnum(CalendarAccessRole, name="calendar_access_role"),  # type: ignore
        nullable=False,
        default=CalendarAccessRole.GUEST,
    )
    created_by = Column[UUID](GUID, ForeignKey("users.id", ondelete="SET NULL"))
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
    calendar = relationship("Calendar", back_populates="access_list")
    user = relationship("User", back_populates="accesses", foreign_keys=[user_id])
