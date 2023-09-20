from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chronal_api.lib.database import mixins, types
from chronal_api.lib.database.engine import Base

from .security import generate_token, generate_token_expiration_date

if TYPE_CHECKING:
    from chronal_api.users.models import User


class AccessToken(Base, mixins.TimestampMixin):
    __tablename__ = "access_tokens"

    access_token: Mapped[str] = mapped_column(
        String(1024), primary_key=True, default=generate_token
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users_.id"), index=True)
    expiration_date: Mapped[datetime] = mapped_column(
        types.DateTimeUTC,
        default=generate_token_expiration_date,
    )

    user: Mapped["User"] = relationship("User", lazy="joined")
