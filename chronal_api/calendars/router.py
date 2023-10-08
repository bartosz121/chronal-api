from uuid import UUID

from fastapi import Depends, HTTPException, Response, status

from chronal_api.lib import router as lib_router
from chronal_api.lib import schemas as api_schemas
from chronal_api.lib.auth import dependencies as auth_dependencies

from . import dependencies, exceptions, schemas

router = lib_router.APIRouter(
    tags=["calendars"],
    dependencies=[Depends(auth_dependencies.get_current_user)],
    api_routes_responses={
        "calendars:list": {
            status.HTTP_200_OK: {
                "description": "List of user calendars",
                "model": list[schemas.CalendarRead],
            },
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Unauthorized",
                "model": api_schemas.Message,
                "content": {"application/json": {"example": {"msg": "Unauthorized"}}},
            },
        },
        "calendars:get_by_id": {
            status.HTTP_200_OK: {
                "description": "Calendar data",
                "model": schemas.CalendarRead,
            },
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Unauthorized",
                "model": api_schemas.Message,
                "content": {"application/json": {"example": {"msg": "Unauthorized"}}},
            },
            status.HTTP_403_FORBIDDEN: {
                "description": "You don't have access to that calendar",
                "model": api_schemas.Message,
                "content": {
                    "application/json": {"example": {"msg": exceptions.HTTPError.FORBIDDEN}}
                },
            },
            status.HTTP_404_NOT_FOUND: {
                "description": "Calendar not found",
                "model": api_schemas.Message,
                "content": {
                    "application/json": {
                        "example": {"msg": exceptions.HTTPError.CALENDAR_NOT_FOUND}
                    }
                },
            },
        },
        "calendars:create": {
            status.HTTP_201_CREATED: {
                "description": "Calendar successfully created",
                "model": schemas.CalendarRead,
            },
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Unauthorized",
                "model": api_schemas.Message,
                "content": {"application/json": {"example": {"msg": "Unauthorized"}}},
            },
            status.HTTP_409_CONFLICT: {
                "description": "Calendar with given name already exists",
                "model": api_schemas.Message,
                "content": {
                    "application/json": {"example": {"msg": exceptions.HTTPError.TITLE_NOT_UNIQUE}}
                },
            },
        },
        "calendars:update": {
            status.HTTP_200_OK: {
                "description": "Calendar successfully updated",
                "model": schemas.CalendarRead,
            },
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Unauthorized",
                "model": api_schemas.Message,
                "content": {"application/json": {"example": {"msg": "Unauthorized"}}},
            },
            status.HTTP_403_FORBIDDEN: {
                "description": "You don't have access to that calendar",
                "model": api_schemas.Message,
                "content": {
                    "application/json": {"example": {"msg": exceptions.HTTPError.FORBIDDEN}}
                },
            },
            status.HTTP_404_NOT_FOUND: {
                "description": "Calendar not found",
                "model": api_schemas.Message,
                "content": {
                    "application/json": {
                        "example": {"msg": exceptions.HTTPError.CALENDAR_NOT_FOUND}
                    }
                },
            },
            status.HTTP_409_CONFLICT: {
                "description": "Calendar with given name already exists",
                "model": api_schemas.Message,
                "content": {
                    "application/json": {"example": {"msg": exceptions.HTTPError.TITLE_NOT_UNIQUE}}
                },
            },
        },
        "calendars:delete": {
            status.HTTP_204_NO_CONTENT: {"description": "Calendar successfully removed"},
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Unauthorized",
                "model": api_schemas.Message,
                "content": {"application/json": {"example": {"msg": "Unauthorized"}}},
            },
            status.HTTP_403_FORBIDDEN: {
                "description": "You don't have access to that calendar",
                "model": api_schemas.Message,
                "content": {
                    "application/json": {"example": {"msg": exceptions.HTTPError.FORBIDDEN}}
                },
            },
            status.HTTP_404_NOT_FOUND: {
                "description": "Calendar not found",
                "model": api_schemas.Message,
                "content": {
                    "application/json": {
                        "example": {"msg": exceptions.HTTPError.CALENDAR_NOT_FOUND}
                    }
                },
            },
        },
    },
)


@router.get("", name="calendars:list", response_model=list[schemas.CalendarRead])
async def list_users_calendars(
    user: auth_dependencies.CurrentUser, calendar_service: dependencies.CalendarService
):
    calendars = await calendar_service.list_(owner_id=user.id)
    return calendars


@router.get("/{id}", name="calendars:get_by_id", response_model=schemas.CalendarRead)
async def get_calendar_by_id(
    id: UUID,
    user: auth_dependencies.CurrentUser,
    calendar_service: dependencies.CalendarService,
    calendar: dependencies.get_calendar_or_404,
):
    if not await calendar_service.is_calendar_owner(user.id, id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "msg": exceptions.HTTPError.FORBIDDEN,
            },
        )

    return calendar


@router.post(
    "",
    name="calendars:create",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CalendarRead,
)
async def create_calendar(
    data: schemas.CalendarCreate,
    user: auth_dependencies.CurrentUser,
    calendar_service: dependencies.CalendarService,
):
    try:
        calendar = await calendar_service.create_calendar(data, user.id)
    except exceptions.TitleNotUnique:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"msg": exceptions.HTTPError.TITLE_NOT_UNIQUE},
        )
    else:
        return calendar


@router.patch("/{id}", name="calendars:update", response_model=schemas.CalendarRead)
async def update_calendar(
    id: UUID,
    data: schemas.CalendarPatch,
    user: auth_dependencies.CurrentUser,
    calendar_service: dependencies.CalendarService,
    calendar: dependencies.get_calendar_or_404,
):
    if not await calendar_service.is_calendar_owner(user.id, calendar.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "msg": exceptions.HTTPError.FORBIDDEN,
            },
        )

    try:
        calendar = await calendar_service.update_calendar(calendar, data)
    except exceptions.TitleNotUnique:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"msg": exceptions.HTTPError.TITLE_NOT_UNIQUE},
        )
    else:
        return calendar


@router.delete(
    "/{id}",
    name="calendars:delete",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    dependencies=[Depends(dependencies._get_calendar_or_404)],
)
async def delete_calendar(
    id: UUID,
    user: auth_dependencies.CurrentUser,
    calendar_service: dependencies.CalendarService,
):
    if not await calendar_service.is_calendar_owner(user.id, id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "msg": exceptions.HTTPError.FORBIDDEN,
            },
        )

    await calendar_service.delete_calendar(id)
