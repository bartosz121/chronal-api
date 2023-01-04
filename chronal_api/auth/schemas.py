import re
import uuid

import pendulum
from fastapi_users import schemas
from pydantic import validator
from pydantic.fields import ModelField

from chronal_api.core.config import get_config

TIMEZONES = pendulum.timezones  # type: ignore
config = get_config()


def check_for_not_allowed_name(value: str, field: ModelField) -> str:
    for name in config.PDNT_BLACKLIST_NAMES:
        if re.search(f"{name}", value):
            raise ValueError(f"This {repr(field.name)} is not allowed")
    return value


class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: str
    last_name: str
    timezone: str


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    timezone: str

    _validated_texts = validator(
        "email", "first_name", "last_name", allow_reuse=True, pre=True
    )(check_for_not_allowed_name)

    @validator("timezone")
    def check_timezone(cls, v: str) -> str:
        if v not in TIMEZONES:
            raise ValueError("Wrong timezone")
        return v


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str
    last_name: str
    timezone: str

    _validated_texts = validator(
        "email", "first_name", "last_name", allow_reuse=True, pre=True
    )(check_for_not_allowed_name)
