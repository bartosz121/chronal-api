from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from chronal_api.auth.dependencies import get_user
from chronal_api.auth.models import User
from chronal_api.calendar_access.dependencies import (
    has_calendar_access,
    has_modify_access,
)
from chronal_api.calendar_access.models import CalendarAccess, CalendarAccessRole
from chronal_api.core.db.dependencies import get_db_session

from .models import Event
from .service import EventService


async def get_events_service(session: AsyncSession = Depends(get_db_session)):
    return EventService(session, Event)


async def valid_event_id(
    event_id: str, service: EventService = Depends(get_events_service)
) -> Event:
    """
    `Depends: get_events_service`
    """
    event = await service.get_by_id(event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )
    return event


async def has_access_to_modify_event(
    user: User = Depends(get_user),
    event: Event = Depends(valid_event_id),
    access: CalendarAccess = Depends(has_calendar_access),
) -> CalendarAccess:
    """
    FIXME
    `Depends: get_user, valid_event_id, has_calendar_access`
    """
    if (
        user.is_superuser
        or access.role
        in (CalendarAccessRole.OWNER.value, CalendarAccessRole.MODERATOR.value)
        or event.created_by == user.id
    ):
        return access
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


# FIXME rename to is_guest???
async def has_access_to_create_event(
    access: CalendarAccess = Depends(has_calendar_access),
) -> CalendarAccess:
    if access.role == CalendarAccessRole.GUEST.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have sufficient access",
        )
    return access
