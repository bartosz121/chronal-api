import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from chronal_api.auth.schemas import UserRead
from chronal_api.calendar_access.schemas import CalendarAccessRead


class BaseCalendar(BaseModel):
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "My Calendar #1",
                "description": "My calendar description",
            }
        }


class CalendarRead(BaseCalendar):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": "e640f6e3-35c7-41d2-9851-0ddac4f09708",
                "name": "Calendar name",
                "description": "Calendar description",
                "owner_id": "61575bf4-1641-4468-abcc-9b98ec1a8182",
                "created_at": "2022-11-27T19:01:21.382752",
                "updated_at": "2022-11-27T19:01:21.382752",
            }
        }


class CalendarReadWithOwner(CalendarRead):
    owner: UserRead


class CalendarReadWithAccess(CalendarRead):
    access: CalendarAccessRead


class CalendarCreate(BaseCalendar):
    owner_id: uuid.UUID | None = None


class CalendarUpdate(BaseCalendar):
    name: Optional[str]
    description: Optional[str]
