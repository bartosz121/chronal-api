import orjson
import pendulum
from pendulum.date import Date
from pendulum.datetime import DateTime
from pendulum.duration import Duration
from pendulum.time import Time
from pydantic import BaseModel

TIMEZONES = pendulum.timezones  # type: ignore


def orjson_dumps(v, *, default):
    """
    orjson.dumps() returns bytes; decode to match standard json.dumps()
    """
    return orjson.dumps(v, default=default).decode()


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ResourceUrl(ORJSONModel):
    resource_url: str


class ExceptionModel(ORJSONModel):
    detail: str


# Reusable validators


def is_timezone_invalid(cls, timezone: str) -> str:
    if timezone not in TIMEZONES:
        raise ValueError("Invalid timezone")
    return timezone


def is_datetime_in_the_past(cls, dt: DateTime) -> DateTime:
    """
    Assumes that `dt` is in UTC
    """
    now = pendulum.now(tz="Etc/UTC")
    if now > dt:
        raise ValueError(f"Time: {dt} is in the past")
    return dt


def set_dt_to_utc(cls, v: str) -> Date | Time | DateTime | Duration:
    """
    Used in EventCreate pre=True validator to set all incoming datetimes as utc

    FIXME find better way to do this
        - waiting for pydantic V2 with custom encoding/decoding
    """
    try:
        dt = pendulum.parser.parse(v)
        if isinstance(dt, DateTime):
            dt = dt.in_tz("Etc/UTC")
    except Exception:  # FIXME
        raise ValueError(f"Could not parse as {v} date time")
    return dt
