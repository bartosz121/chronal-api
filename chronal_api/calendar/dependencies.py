import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from chronal_api.calendar.models import Calendar
from chronal_api.core.abc import UUID
from chronal_api.core.db.dependencies import get_db_session

from .service import CalendarService

logger = logging.getLogger()


async def get_calendar_service(
    session: AsyncSession = Depends(get_db_session),
) -> CalendarService:
    """
    `Returns: CalendarService`
    `Depends: get_db_session`
    """
    return CalendarService(session, Calendar)


async def valid_calendar_id(
    calendar_id: UUID,
    service: CalendarService = Depends(get_calendar_service),
) -> Calendar:
    """
    `Returns: Calendar`
    `Depends on: get_calendar_service`
    """
    try:
        calendar_db = await service.get_by_id(calendar_id)
        if calendar_db is None:
            raise ValueError("Not found")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    else:
        return calendar_db
