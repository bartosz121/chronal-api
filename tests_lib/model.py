from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(
    AsyncAttrs,
    DeclarativeBase,
):
    pass


class TodoItem(Base):
    __tablename__ = "todo_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    is_complete: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )

    def __repr__(
        self,
    ) -> str:
        return f"<TodoItem(id={self.id}, title={self.title}, description={self.description}, is_complete={self.is_complete})>"
