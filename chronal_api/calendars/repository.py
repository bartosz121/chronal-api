from uuid import UUID

from chronal_api.lib.repository.sqlalchemy import SQLAlchemyRepository

from .models import Calendar


class CalendarRepository(SQLAlchemyRepository):
    model = Calendar

    async def user_is_calendar_owner(self, user_id: UUID, calendar_id: UUID) -> bool:
        return await self.exists(id=calendar_id, owner_id=user_id)

    async def title_exists_for_user(self, user_id: UUID, title: str) -> bool:
        return await self.exists(owner_id=user_id, title=title)
