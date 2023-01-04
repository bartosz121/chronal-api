import uuid
from typing import Any, Generic, Iterable, Optional, TypeVar

from sqlalchemy import delete as sqla_delete
from sqlalchemy import update as sqla_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import RelationshipProperty

from chronal_api.schemas import ORJSONModel

from .db import Base

UUID = uuid.UUID | str

Model = TypeVar("Model", bound=Base)
CreateSchema = TypeVar("CreateSchema", bound=ORJSONModel)
UpdateSchema = TypeVar("UpdateSchema", bound=ORJSONModel)


class BaseService(Generic[Model, CreateSchema, UpdateSchema]):
    def __init__(self, session: AsyncSession, model: type[Model]) -> None:
        self.session = session
        self.model = model

    async def get(
        self,
        first: bool = False,
        fields: Optional[Iterable[RelationshipProperty]] = None,
        options: Optional[Iterable[Any]] = None,
        **filter_by,
    ) -> list[Model] | Model:
        q = select(*fields) if fields else select(self.model)
        if options:
            q = q.options(*options)

        r = await self.session.scalars(q.filter_by(**filter_by))

        return r.one_or_none() if first else r.all()

    async def get_by_id(
        self, id: UUID, options: Optional[Iterable[Any]] = None
    ) -> Optional[Model]:
        return await self.session.get(self.model, id, options=options)

    async def get_all(
        self, options: Optional[Iterable[Any]] = None, **kwargs
    ) -> list[Model]:
        q = select(self.model).options(*options) if options else select(self.model)
        r = await self.session.scalars(q, **kwargs)
        data = r.all()

        return data

    async def create(self, data: CreateSchema) -> UUID:
        obj = self.model(**data.dict())
        self.session.add(obj)
        await self.session.flush()

        return obj.id

    async def update(self, obj_id: UUID, data: UpdateSchema) -> UUID:
        await self.session.execute(
            sqla_update(self.model).where(self.model.id == obj_id).values(**data.dict())
        )

        return obj_id

    async def delete(self, obj_id: UUID) -> None:
        await self.session.execute(
            sqla_delete(self.model).where(self.model.id == obj_id)
        )
