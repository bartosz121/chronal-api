import logging

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from chronal_api.auth.dependencies import get_superuser, get_user
from chronal_api.auth.models import User
from chronal_api.calendar_access.dependencies import (
    before_delete_check,
    has_access_to_calendar_access,
)
from chronal_api.calendar_access.schemas import CalendarAccessRead
from chronal_api.utils import create_router_prefix

from .dependencies import get_calendar_access_service
from .models import CalendarAccess
from .service import CalendarAccessService

logger = logging.getLogger()

router = APIRouter(
    prefix=create_router_prefix("/calendars-access"),
    tags=[
        "calendar-access",
    ],
    dependencies=[
        Depends(get_user),
    ],
)


@router.get(
    "/", response_model=list[CalendarAccessRead], dependencies=[Depends(get_superuser)]
)
async def get_all(
    service: CalendarAccessService = Depends(get_calendar_access_service),
):
    all_ca = await service.get_all()
    return all_ca


@router.get(
    "/me",
    response_model=list[CalendarAccessRead],
)
async def get_user_access_list(
    user: User = Depends(get_user),
    service: CalendarAccessService = Depends(get_calendar_access_service),
):
    all_ca = await service.get_access_list_for_user(user.id)
    return all_ca


@router.get(
    "/user/{user_id}",
    response_model=list[CalendarAccessRead],
    dependencies=[Depends(get_superuser)],
)
async def get_access_list_by_user(
    user_id: str,
    service: CalendarAccessService = Depends(get_calendar_access_service),
):
    user_ca = await service.get_access_list_for_user(user_id)
    return user_ca


@router.get(
    "/{calendar_access_id}",
    response_model=CalendarAccessRead,
)
async def get_calendar_access_by_id(
    calendar_access_id: str,
    ca: CalendarAccess = Depends(has_access_to_calendar_access),
):
    return ca


@router.delete(
    "/{calendar_id}/{calendar_access_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_204_NO_CONTENT: {"model": None}},
    dependencies=[
        Depends(before_delete_check),
    ],
)
async def delete_calendar_access(
    calendar_access_id: str,
    service: CalendarAccessService = Depends(get_calendar_access_service),
):
    await service.delete(calendar_access_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
