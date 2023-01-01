import logging
from typing import Optional

from sqlalchemy.orm import joinedload, selectinload

from chronal_api.core.abc import UUID, BaseService

from .models import Calendar
from .schemas import CalendarCreate, CalendarUpdate

logger = logging.getLogger()


class CalendarService(BaseService[Calendar, CalendarCreate, CalendarUpdate]):
    async def get_user_calendars(self, user_id: UUID) -> list[Calendar]:
        calendars = await self.get(owner_id=user_id)
        return calendars

    async def get_all_with_owner(self) -> list[Calendar]:
        calendars = await self.get_all(options=(selectinload(Calendar.owner),))
        return calendars
