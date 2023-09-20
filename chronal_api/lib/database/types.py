import datetime
import uuid
from typing import Any

from pydantic import UUID4
from sqlalchemy import CHAR as sqla_CHAR
from sqlalchemy import TIMESTAMP as sqla_TIMESTAMP
from sqlalchemy import types as sqla_types
from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.sql.type_api import TypeEngine


class UUID(sqla_types.TypeDecorator):
    """
    UUID for sqlite
    """

    class UUIDChar(sqla_CHAR):
        python_type = UUID4  # pyright: ignore

    impl = UUIDChar
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine[Any]:
        return dialect.type_descriptor(sqla_CHAR(36))

    def process_bind_param(self, value: Any | None, dialect: Dialect) -> Any:
        if not isinstance(value, uuid.UUID):
            if value is None:
                return None
            breakpoint()
            return str(uuid.UUID(value))
        return str(value)

    def process_result_value(self, value: Any | None, dialect: Dialect) -> Any | None:
        if value is not None:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
        return value


class DateTimeUTC(sqla_types.TypeDecorator):  # pyright: ignore
    impl = sqla_TIMESTAMP
    cache_ok = True

    def process_bind_param(self, value: datetime.datetime | None, dialect: Dialect) -> Any:
        if not isinstance(value, datetime.datetime):
            if value is None:
                return None
            raise TypeError(f"Expected datetime.datetime, not {value!r}")
        elif value.tzinfo is None:
            raise ValueError("Naive datetime not allowed")
        return value.astimezone(datetime.timezone.utc)

    def process_result_value(
        self, value: datetime.datetime | None, dialect: Dialect
    ) -> Any | None:
        if value is not None:
            if value.tzinfo is None:
                value = value.replace(tzinfo=datetime.timezone.utc)
            else:
                value = value.astimezone(datetime.timezone.utc)
        return value
