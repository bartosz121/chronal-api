import logging
from typing import Any, Iterable, Optional

from sqlalchemy.orm import RelationshipProperty, selectinload

from chronal_api.core.abc import UUID, BaseService

from .models import CalendarAccess
from .schemas import CalendarAccessCreateDb, CalendarAccessUpdate

logger = logging.getLogger()


class CalendarAccessService(
    BaseService[CalendarAccess, CalendarAccessCreateDb, CalendarAccessUpdate]
):
    async def get_calendar_access_for_user(
        self,
        calendar_id: UUID,
        user_id: UUID,
    ) -> CalendarAccess:
        ca = await self.get(
            first=True,
            calendar_id=calendar_id,
            user_id=user_id,
        )

        if ca is None:
            raise ValueError(
                f"Access for user {user_id} in calendar {calendar_id} not found"
            )
        return ca

    async def get_access_list_for_calendar(
        self, calendar_id: UUID
    ) -> list[CalendarAccess]:
        ca_list = await self.get(calendar_id=calendar_id)
        return ca_list

    async def get_access_list_for_user(self, user_id: UUID) -> list[CalendarAccess]:
        ca_list = await self.get(user_id=user_id)
        return ca_list
