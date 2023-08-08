# mostly stolen from https://github.com/litestar-org/litestar/blob/2744bf4b8fb7d8b8886229aa71fa1ee8d9a3ffde/litestar/contrib/repository/abc/_async.py

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Coroutine, Generic, Sequence, TypeVar
from uuid import UUID

from sqlalchemy import Column
from sqlalchemy import func as sqla_func
from sqlalchemy import select

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")
U = TypeVar("U")


class Repository(Generic[T, U], ABC):
    model: type[T]
    model_id_attr_name: str = "id"
    model_id_type: type[U]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    @property
    def model_id_attr(self) -> Column[U]:
        return getattr(self.model, self.model_id_attr_name)

    @abstractmethod
    async def count(self) -> int:
        """
        Count the number of records in the table.

        Returns:
            int: The number of records in the table.
        """

    @abstractmethod
    async def create(self, data: T) -> T:
        """
        Create a record in the table.

        Args:
            data (T): The data to create the record with.

        Returns:
            T: The created record.
        """

    @abstractmethod
    async def create_many(self, data: Sequence[T]) -> list[T]:
        """
        Create many records in the table.

        Args:
            data (Sequence[T]): The data to create the records with.

        Returns:
            list[T]: The created records.
        """

    @abstractmethod
    async def delete(self, id: U) -> T:
        """
        Delete a record from the table.

        Args:
            id (U): The ID of the record to delete.

        Returns:
            T: The deleted record.

        Raises:
            NotFoundError: If no record is found.
        """

    @abstractmethod
    async def delete_many(self, ids: Sequence[U]) -> list[T]:
        """
        Delete many records from the table.

        Args:
            ids (Sequence[U]): The IDs of the records to delete.

        Returns:
            list[T]: The deleted records.
        """

    @abstractmethod
    async def exists(self, **kwargs: Any) -> bool:
        """
        Check if a record exists in the table.

        Args:
            **kwargs (Any): The query parameters to check for.

        Returns:
            bool: Whether or not the record exists.
        """

    @abstractmethod
    async def get(self, id: U, **kwargs: Any) -> T:
        """
        Get a record from the table.

        Args:
            id (U): The ID of the record to get.
            **kwargs (Any): The query parameters to get the record with.

        Returns:
            T: The record.

        Raises:
            NotFoundError: If no record is found.
        """

    @abstractmethod
    async def get_one(self, id: U, **kwargs: Any) -> T:
        """
        Get a record from the table.

        Args:
            id (U): The ID of the record to get.
            **kwargs (Any): The query parameters to get the record with.

        Returns:
            T: The record.

        Raises:
            NotFoundError: If no record is found.
        """

    @abstractmethod
    async def get_one_or_none(self, id: U, **kwargs: Any) -> T | None:
        """
        Get a record from the table.

        Args:
            id (U): The ID of the record to get.
            **kwargs (Any): The query parameters to get the record with.

        Returns:
            T | None: The record.
        """

    @abstractmethod
    async def list_(self, **kwargs: Any) -> list[T]:  # FIXME: pylance shows error without '_' because it shadows `list`
        """
        List records from the table.

        Args:
            **kwargs (Any): The query parameters to list the records with.

        Returns:
            list[T]: The records.
        """

    @abstractmethod
    async def list_and_count(self, **kwargs: Any) -> tuple[list[T], int]:
        """
        List records from the table.

        Args:
            **kwargs (Any): The query parameters to list the records with.

        Returns:
            tuple[list[T], int]: The records and the count.
        """

    @abstractmethod
    async def update(self, data: T) -> T:
        """
        Update a record in the table.

        Args:
            data (T): The data to update the record with.

        Returns:
            T: The updated record.

        Raises:
            NotFoundError: If no record is found.
        """

    @abstractmethod
    async def update_many(self, data: Sequence[T]) -> list[T]:
        """
        Update many records in the table.

        Args:
            data (Sequence[T]): The data to update the records with.

        Returns:
            list[T]: The updated records.
        """

    @abstractmethod
    async def upsert(self, data: T) -> T:
        """
        Upsert a record in the table.

        Args:
            data (T): The data to upsert the record with.

        Returns:
            T: The upserted record.
        """

    @abstractmethod
    async def upsert_many(self, data: Sequence[T]) -> list[T]:
        """
        Upsert many records in the table.

        Args:
            data (Sequence[T]): The data to upsert the records with.

        Returns:
            list[T]: The upserted records.
        """


class SQLAlchemyRepository(Repository[T, U]):
    def __init__(self, session: "AsyncSession", *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.session = session
        self.statement = select(self.model)

    async def count(self) -> int:
        s = self.statement.with_only_columns(
            sqla_func.count(self.model_id_attr),
            maintain_column_froms=True,
        ).order_by(None)
        result = await self.session.execute(s)
        return result.scalar_one()

    async def create(self, data: T) -> T:
        return await super().create(data)

    async def create_many(self, data: Sequence[T]) -> list[T]:
        return await super().create_many(data)

    async def delete(self, id: U) -> T:
        return await super().delete(id)

    async def delete_many(self, ids: Sequence[U]) -> list[T]:
        return await super().delete_many(ids)

    async def exists(self, **kwargs: Any) -> bool:
        return await super().exists(**kwargs)

    async def get(self, id: U, **kwargs: Any) -> T:
        return await super().get(id, **kwargs)

    async def get_one(self, id: U, **kwargs: Any) -> T:
        return await super().get_one(id, **kwargs)

    async def get_one_or_none(self, id: U, **kwargs: Any) -> T | None:
        return await super().get_one_or_none(id, **kwargs)

    async def list_(self, **kwargs: Any) -> list[T]:
        return await super().list_(**kwargs)

    async def list_and_count(self, **kwargs: Any) -> tuple[list[T], int]:
        return await super().list_and_count(**kwargs)

    async def update(self, data: T) -> T:
        return await super().update(data)

    async def update_many(self, data: Sequence[T]) -> list[T]:
        return await super().update_many(data)

    async def upsert(self, data: T) -> T:
        return await super().upsert(data)

    async def upsert_many(self, data: Sequence[T]) -> list[T]:
        return await super().upsert_many(data)
