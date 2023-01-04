from datetime import datetime
from typing import Optional

from chronal_api.calendar_access.models import CalendarAccessRole
from chronal_api.core.abc import UUID
from chronal_api.schemas import ORJSONModel


class BaseCalendarAccess(ORJSONModel):
    class Config:
        orm_mode = True


class CalendarAccessRead(BaseCalendarAccess):
    id: UUID
    calendar_id: UUID
    user_id: UUID
    role: CalendarAccessRole
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class CalendarAccessCreateApi(BaseCalendarAccess):
    user_id: UUID
    role: CalendarAccessRole


class CalendarAccessCreateDb(BaseCalendarAccess):
    calendar_id: UUID
    user_id: UUID
    role: CalendarAccessRole
    created_by: UUID


class CalendarAccessUpdate(BaseCalendarAccess):
    calendar_id: Optional[UUID]
    user_id: Optional[UUID]
