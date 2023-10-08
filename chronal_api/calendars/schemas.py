from pydantic import UUID4

from chronal_api.lib import schemas as base_schemas


class CalendarBase(base_schemas.BaseModel):
    id: UUID4


class CalendarCreate(base_schemas.BaseModel):
    title: str
    description: str | None = None


class CalendarRead(CalendarBase):
    title: str
    description: str | None = None


class CalendarPatch(base_schemas.BaseModel):
    title: str | None = None
    descriptipn: str | None = None


__all__ = ["CalendarCreate", "CalendarRead", "CalendarPatch"]
