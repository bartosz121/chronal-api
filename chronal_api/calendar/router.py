import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from fastapi_users.exceptions import UserNotExists

from chronal_api.auth.dependencies import get_superuser, get_user, get_user_manager
from chronal_api.auth.models import User
from chronal_api.auth.user_manager import UserManager
from chronal_api.calendar.dependencies import get_calendar_service, valid_calendar_id
from chronal_api.calendar.models import Calendar
from chronal_api.calendar.schemas import (
    CalendarCreate,
    CalendarRead,
    CalendarReadWithOwner,
    CalendarUpdate,
)
from chronal_api.calendar_access.dependencies import (
    check_if_already_has_access,
    get_calendar_access_service,
    has_calendar_access,
    has_modify_access,
)
from chronal_api.calendar_access.schemas import (
    CalendarAccessCreateApi,
    CalendarAccessCreateDb,
    CalendarAccessRead,
)
from chronal_api.calendar_access.service import CalendarAccessService
from chronal_api.calendar_access.utils import get_path_for as ca_router_get_path_for
from chronal_api.events.router import calendar_events_subrouter
from chronal_api.schemas import ExceptionModel, ResourceUrl
from chronal_api.utils import create_router_prefix

from .service import CalendarService

logger = logging.getLogger()

router = APIRouter(
    prefix=create_router_prefix("/calendars"),
    tags=["calendars"],
    dependencies=[Depends(get_user)],
)


router.include_router(calendar_events_subrouter)


@router.get(
    "/",
    response_model=list[CalendarReadWithOwner],
    dependencies=[Depends(get_superuser)],
)
async def get_calendars(
    service: CalendarService = Depends(get_calendar_service),
):
    all_calendars = await service.get_all_with_owner()

    return all_calendars


@router.get("/me", response_model=list[CalendarRead])
async def get_my_calendars(
    user: User = Depends(get_user),
    service: CalendarService = Depends(get_calendar_service),
):
    calendars = await service.get_user_calendars(user.id)
    return calendars


@router.get(
    "/{calendar_id}",
    response_model=CalendarRead,
    dependencies=[Depends(has_calendar_access)],
)
async def get_calendar_by_id(calendar: Calendar = Depends(valid_calendar_id)):
    return calendar


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResourceUrl)
async def create_calendar(
    data: CalendarCreate,
    user: User = Depends(get_user),
    service: CalendarService = Depends(get_calendar_service),
):
    data.owner_id = user.id
    created_id = await service.create(data)
    return {
        "resource_url": router.url_path_for(
            "get_calendar_by_id", calendar_id=created_id
        )
    }


@router.patch(
    "/{calendar_id}",
    response_model=ResourceUrl,
    dependencies=[Depends(has_modify_access)],
)
async def update_calendar(
    calendar_id: str,
    data: CalendarUpdate,
    service: CalendarService = Depends(get_calendar_service),
):
    await service.update(calendar_id, data)
    return {
        "resource_url": router.url_path_for(
            "get_calendar_by_id", calendar_id=calendar_id
        )
    }


@router.delete(
    "/{calendar_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_204_NO_CONTENT: {"model": None}},
    dependencies=[Depends(has_modify_access)],
)
async def delete_calendar(
    calendar_id: str,
    service: CalendarService = Depends(get_calendar_service),
):
    await service.delete(calendar_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Calendar Access routes =======================================================


@router.get(
    "/{calendar_id}/access",
    response_model=list[CalendarAccessRead],
    dependencies=[Depends(has_calendar_access)],
    tags=["calendar-access"],
)
async def get_calendar_access_list(
    calendar_id: str,
    service: CalendarAccessService = Depends(get_calendar_access_service),
):
    ca_list = await service.get_access_list_for_calendar(calendar_id)
    return ca_list


@router.post(
    "/{calendar_id}/access",
    status_code=status.HTTP_201_CREATED,
    response_model=ResourceUrl,
    dependencies=[
        Depends(has_modify_access),
        Depends(check_if_already_has_access),
    ],
    tags=["calendar-access"],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ExceptionModel,
            "content": {
                "application/json": {
                    "examples": {
                        "User already has access to calendar": {
                            "value": {
                                "detail": "User UUID('f1a06e4d-3e01-4347-bc93-e311df52a376') already has access to this calendar UUID('a166c3c6-085f-4963-b534-18162f768014')"
                            }
                        }
                    }
                }
            },
        }
    },
)
async def create_calendar_access(
    calendar_id: str,
    data: CalendarAccessCreateApi,
    user: User = Depends(get_user),
    user_manager: UserManager = Depends(get_user_manager),
    service: CalendarAccessService = Depends(get_calendar_access_service),
):
    try:
        await user_manager.get(data.user_id)  # type: ignore
    except UserNotExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {data.user_id!r} does not exist",
        )

    create_schema_db = CalendarAccessCreateDb(
        calendar_id=calendar_id,
        user_id=data.user_id,
        role=data.role,
        created_by=user.id,
    )
    ca_id = await service.create(create_schema_db)
    return {
        "resource_url": ca_router_get_path_for(
            "get_calendar_access_by_id", calendar_access_id=ca_id
        )
    }
