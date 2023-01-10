import uuid
from typing import Optional

from pendulum.datetime import DateTime
from pydantic import root_validator, validator

from chronal_api.core.abc import UUID
from chronal_api.schemas import (
    ORJSONModel,
    is_datetime_in_the_past,
    is_timezone_invalid,
    set_dt_to_utc,
)

# TODO reuse model with validation


class EventBase(ORJSONModel):
    title: str
    description: Optional[str]
    timezone: str
    start_dt: DateTime
    end_dt: DateTime

    class Config:
        orm_mode = True
        # schema_extra = {"example": {}}


class EventRead(EventBase):
    id: UUID
    created_by: UUID
    calendar_id: UUID
    created_at: DateTime
    updated_at: DateTime


class EventCreate(EventBase):
    created_by: uuid.UUID | None = None
    calendar_id: uuid.UUID

    _set_to_utc = validator("start_dt", "end_dt", allow_reuse=True, pre=True)(
        set_dt_to_utc
    )

    _validate_timezone = validator("timezone", allow_reuse=True, pre=True)(
        is_timezone_invalid
    )

    _validate_datetimes = validator("start_dt", "end_dt", allow_reuse=True)(
        is_datetime_in_the_past
    )

    @root_validator()
    def check_datetimes(cls, values):
        start_dt: DateTime = values.get("start_dt")
        end_dt: DateTime = values.get("end_dt")

        if start_dt is not None and end_dt is not None:
            if start_dt > end_dt:
                raise ValueError("The end time of the event is before the start time")
            if start_dt == end_dt:
                raise ValueError(
                    "The end time is the same as the start time of the event"
                )
        return values


class EventUpdate(ORJSONModel):
    title: Optional[str]
    description: Optional[str]
    timezone: Optional[str]
    start_dt: Optional[DateTime]
    end_dt: Optional[DateTime]

    class Config:
        orm_mode = True

    _set_to_utc = validator("start_dt", "end_dt", allow_reuse=True, pre=True)(
        set_dt_to_utc
    )

    _validate_timezone = validator("timezone", allow_reuse=True, pre=True)(
        is_timezone_invalid
    )

    _validate_datetimes = validator("start_dt", "end_dt", allow_reuse=True)(
        is_datetime_in_the_past
    )

    @root_validator()
    def check_datetimes(cls, values):
        start_dt: DateTime = values.get("start_dt")
        end_dt: DateTime = values.get("end_dt")

        if start_dt is not None and end_dt is not None:
            if start_dt > end_dt:
                raise ValueError("The end time of the event is before the start time")
            if start_dt == end_dt:
                raise ValueError(
                    "The end time is the same as the start time of the event"
                )
        return values


class EventDelete(ORJSONModel):
    id: UUID
