from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from chronal_api.lib.database import mixins
from chronal_api.lib.database.engine import Base


class User(Base, mixins.UUIDPrimaryKeyMixin, mixins.TimestampMixin):
    __tablename__ = "users_"

    email: Mapped[str] = mapped_column(String(length=255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024))
