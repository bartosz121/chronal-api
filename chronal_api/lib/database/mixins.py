from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from chronal_api.lib.database import types as db_types


def utc_now():
    return datetime.now(timezone.utc)


class UUIDPrimaryKeyMixin:
    id: Mapped[UUID] = mapped_column(db_types.UUID, default=uuid4, primary_key=True)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        db_types.DateTimeUTC(timezone=True),
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        db_types.DateTimeUTC(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )
