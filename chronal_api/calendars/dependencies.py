from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status

from chronal_api.calendars import models as calendars_models
from chronal_api.lib.database import dependencies as db_dependencies

from . import exceptions, repository, service


async def calendar_service(session: db_dependencies.DbSession) -> service.CalendarService:
    return service.CalendarService(repository.CalendarRepository(session))


async def _get_calendar_or_404(
    id: UUID,
    service: service.CalendarService = Depends(calendar_service),
) -> calendars_models.Calendar:
    calendar = await service.get_one_or_none(id)
    if calendar is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": exceptions.HTTPError.CALENDAR_NOT_FOUND},
        )
    return calendar


# Annotated

CalendarService = Annotated[service.CalendarService, Depends(calendar_service)]
get_calendar_or_404 = Annotated[calendars_models.Calendar, Depends(_get_calendar_or_404)]


__all__ = ["CalendarService", "get_calendar_or_404"]
