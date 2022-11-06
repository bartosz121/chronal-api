import uuid
from datetime import datetime

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: str
    last_name: str
    timezone: str
    created_at: datetime
    updated_at: datetime


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    timezone: str


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str
    last_name: str
    timezone: str
