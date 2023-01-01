import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from chronal_api.auth.dependencies import get_user
from chronal_api.auth.models import User
from chronal_api.calendar.dependencies import valid_calendar_id
from chronal_api.calendar.models import Calendar
from chronal_api.core.abc import UUID
from chronal_api.core.db.dependencies import get_db_session

from .models import CalendarAccess, CalendarAccessRole
from .schemas import CalendarAccessCreateApi
from .service import CalendarAccessService

logger = logging.getLogger()


async def get_calendar_access_service(session: AsyncSession = Depends(get_db_session)):
    """
    `Returns: CalendarAccessService`
    `Depends: get_db_session`
    """
    return CalendarAccessService(session, CalendarAccess)


async def valid_calendar_access_id(
    calendar_access_id: UUID,
    service: CalendarAccessService = Depends(get_calendar_access_service),
) -> CalendarAccess:
    """
    `Returns: CalendarAccess`
    `Depends: get_calendar_access_service`
    """
    try:
        calendar_access = await service.get_by_id(calendar_access_id)
        print(f"{calendar_access=}")
        if calendar_access is None:
            raise ValueError("Not found")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    else:
        return calendar_access


async def has_access_to_calendar_access(
    user: User = Depends(get_user),
    calendar_access: CalendarAccess = Depends(valid_calendar_access_id),
):
    """
    Bad name but all it does is - check if user_id is user.id or user is superuser or user.id is created_by

    `Returns: CalendarAccess`
    `Depends: get_user, valid_calendar_access_id`
    """
    if (
        user.is_superuser
        or calendar_access.user_id == user.id
        or calendar_access.created_by == user.id
    ):
        return calendar_access
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You don't have access to this resource",
    )


async def has_calendar_access_by_calendar_access_id(
    user: User = Depends(get_user),
    calendar_access: CalendarAccess = Depends(valid_calendar_access_id),
    service: CalendarAccessService = Depends(get_calendar_access_service),
) -> CalendarAccess:
    """
    `Returns: CalendarAccess`
    `Depends on: get_user, valid_calendar_access_id, get_calendar_access_service`
    """
    user_access = await service.get(
        first=True, calendar_id=calendar_access.calendar_id, user_id=user.id
    )

    if user_access is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have access to this resource",
        )

    return user_access


async def has_calendar_access(
    service: CalendarAccessService = Depends(get_calendar_access_service),
    user: User = Depends(get_user),
    calendar: Calendar = Depends(valid_calendar_id),
) -> CalendarAccess:
    """
    Check if `user` has access to calendar or is superuser

    `Returns: CalendarAccess`
    `Depends: get_calendar_access_service, get_user, valid_calendar_id`
    """
    if user.is_superuser:
        return CalendarAccess

    try:
        access = await service.get_calendar_access_for_user(calendar.id, user.id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"You dont have access to this calendar {calendar.id!r}",
        )
    else:
        return access


async def has_owner_access(
    user: User = Depends(get_user),
    calendar_access: CalendarAccess = Depends(has_calendar_access),
) -> CalendarAccess:
    """
    `Returns: CalendarAccess`
    `Depends: has_calendar_access`
    """
    if user.is_superuser:
        return calendar_access

    if calendar_access.role != CalendarAccessRole.OWNER.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have sufficient access",
        )
    return calendar_access


async def check_if_already_has_access(
    calendar_id: UUID,
    data: CalendarAccessCreateApi,
    service: CalendarAccessService = Depends(get_calendar_access_service),
) -> CalendarAccess:
    """
    `Returns: CalendarAccess`
    `Depends: get_calendar_access_service`
    """
    ca = await service.get(
        first=True,
        calendar_id=calendar_id,
        user_id=data.user_id,
    )
    if ca:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {data.user_id!r} already has access to this calendar {calendar_id!r}",
        )
    return ca


async def before_delete_check(
    user: User = Depends(get_user),
    user_calendar_access: CalendarAccess = Depends(has_calendar_access),
    calendar_access: CalendarAccess = Depends(valid_calendar_access_id),
) -> CalendarAccess:
    """
    1. Check if owner is stupid and wants to delete his own access
    2. User with access == STANDARD or GUEST should not be able to delete anything other than their own access
    3. Moderator should not be able to remove owner access

    `Returns: CalendarAccess`
    `Depends: get_user, has_sufficient_access_to_delete, has_owner_access`
    """
    print(f"{vars(user)=}")
    print(f"{vars(user_calendar_access)=}")
    print(f"{vars(calendar_access)=}")
    if user.id == calendar_access.user_id:
        if user_calendar_access.role == CalendarAccessRole.OWNER.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Owner cannot remove his access",
            )
        return calendar_access

    if user_calendar_access.role in (
        CalendarAccessRole.STANDARD.value,
        CalendarAccessRole.GUEST.value,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    else:
        print("in else")
        if (
            user_calendar_access.role == CalendarAccessRole.MODERATOR.value
            and calendar_access.role
            in (CalendarAccessRole.MODERATOR.value, CalendarAccessRole.OWNER.value)
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )
        return calendar_access
