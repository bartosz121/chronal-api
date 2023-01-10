from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from chronal_api.auth.dependencies import get_superuser, get_user
from chronal_api.auth.models import User
from chronal_api.calendar_access.dependencies import (
    has_calendar_access,
    has_modify_access,
)
from chronal_api.calendar_access.models import CalendarAccess
from chronal_api.schemas import ResourceUrl
from chronal_api.utils import create_router_prefix

from .dependencies import (
    get_events_service,
    has_access_to_create_event,
    has_access_to_modify_event,
    valid_event_id,
)
from .models import Event
from .schemas import EventCreate, EventRead, EventUpdate
from .service import EventService

# Events router
events_router = APIRouter(prefix=create_router_prefix("/events"), tags=["events"])


@events_router.get("/", dependencies=[Depends(get_superuser)])
async def get_all_events(service: EventService = Depends(get_events_service)):
    events = await service.get_all()
    return events


@events_router.get("/me", response_model=list[EventRead])
async def get_events_me(
    user: User = Depends(get_user), service: EventService = Depends(get_events_service)
):
    events = await service.get_events_created_by(user.id)
    return events


@events_router.get(
    "/user/{user_id}",
    response_model=list[EventRead],
    dependencies=[Depends(get_superuser)],
)
async def get_events_created_by(
    user_id: str, service: EventService = Depends(get_events_service)
):
    events = await service.get_events_created_by(user_id)
    return events


# Events calendar subrouter
calendar_events_subrouter = APIRouter(tags=["calendar-events"])


@calendar_events_subrouter.get(
    "/{calendar_id}/events",
    response_model=list[EventRead],
    dependencies=[Depends(has_calendar_access)],
)
async def get_events_for_calendar(
    calendar_id: str, service: EventService = Depends(get_events_service)
) -> list[Event]:
    events = await service.get_events_for_calendar(calendar_id)
    return events


@calendar_events_subrouter.get(
    "/{calendar_id}/events/{event_id}",
    response_model=EventRead,
    dependencies=[Depends(has_calendar_access)],
)
async def get_event_by_id(
    calendar_id: str, event_id: str, event: Event = Depends(valid_event_id)
):
    return event


@calendar_events_subrouter.post(
    "/{calendar_id}/events",
    response_model=ResourceUrl,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(has_access_to_create_event)],
)
async def create_event(
    calendar_id: str,
    data: EventCreate,
    user: User = Depends(get_user),
    service: EventService = Depends(get_events_service),
):
    data.created_by = user.id
    created_id = await service.create(data)
    return {
        "resource_url": calendar_events_subrouter.url_path_for(
            "get_event_by_id", calendar_id=calendar_id, event_id=created_id
        )
    }


@calendar_events_subrouter.patch("/{calendar_id}/events/{event_id}")
async def patch_event(
    calendar_id: str,
    event_id: str,
    data: EventUpdate,
    event: Event = Depends(valid_event_id),
    access: CalendarAccess = Depends(has_access_to_modify_event),
    service: EventService = Depends(get_events_service),
):
    await service.update(event_id, data)
    return {
        "resource_url": calendar_events_subrouter.url_path_for(
            "get_event_by_id", calendar_id=calendar_id, event_id=event_id
        )
    }


@calendar_events_subrouter.delete(
    "/{calendar_id}/events/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_204_NO_CONTENT: {"model": None}},
)
async def delete_event_by_id(
    calendar_id: str,
    event_id: str,
    access: CalendarAccess = Depends(has_access_to_modify_event),
    service: EventService = Depends(get_events_service),
):
    await service.delete(event_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
