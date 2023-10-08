from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chronal_api.lib.database import mixins
from chronal_api.lib.database.engine import Base

if TYPE_CHECKING:
    from chronal_api.users.models import User


class Calendar(Base, mixins.UUIDPrimaryKeyMixin, mixins.TimestampMixin):
    __tablename__ = "calendars"

    title: Mapped[str] = mapped_column(String(length=255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users_.id", ondelete="CASCADE"), index=True)

    owner: Mapped["User"] = relationship("User", lazy="raise_on_sql")
