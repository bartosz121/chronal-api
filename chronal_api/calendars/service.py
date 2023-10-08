from uuid import UUID

from chronal_api.lib.service import Service

from . import exceptions, models, repository, schemas


class CalendarService(Service[models.Calendar, UUID]):
    def __init__(self, repository: repository.CalendarRepository) -> None:
        self.repository = repository

    async def is_calendar_owner(self, user_id: UUID, calendar_id: UUID) -> bool:
        is_owner = await self.repository.user_is_calendar_owner(user_id, calendar_id)
        return is_owner

    async def create_calendar(
        self, data: schemas.CalendarCreate, user_id: UUID
    ) -> models.Calendar:
        if await self.repository.title_exists_for_user(user_id, data.title):
            raise exceptions.TitleNotUnique()

        calendar = models.Calendar(**data.model_dump(), owner_id=user_id)
        calendar_db = await self.create(calendar)
        return calendar_db

    async def update_calendar(
        self, calendar: models.Calendar, data: schemas.CalendarPatch
    ) -> models.Calendar:
        if data.title:
            if await self.repository.title_exists_for_user(calendar.owner_id, data.title):
                raise exceptions.TitleNotUnique()

        for field_name, value in data.model_dump(exclude_unset=True).items():
            setattr(calendar, field_name, value)

        calendar_db = await self.repository.update(calendar)
        return calendar_db

    async def delete_calendar(self, id: UUID) -> None:
        await self.repository.delete(id)
