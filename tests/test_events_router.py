import pendulum
import pytest
from fastapi import status
from httpx import AsyncClient

from chronal_api.calendar_access.models import CalendarAccessRole

from .data import (
    AUTH_CLIENT_USER0,
    AUTH_CLIENT_USER0_ACCESS_LIST,
    AUTH_CLIENT_USER0_CALENDARS,
    AUTH_CLIENT_USER1,
    AUTH_CLIENT_USER1_ACCESS_LIST,
    AUTH_CLIENT_USER3,
    CALENDAR_IDS_BY_USER_ID,
    EVENTS_BY_CALENDAR_ID,
    EVENTS_BY_USER_ID,
    USER_ACCESS_CALENDAR_IDS_BY_USER_ID,
    calendar_access_objs,
    calendar_objs,
    event_objs,
)


# Events router
@pytest.mark.asyncio
async def test_events_all_superuser(superuser_client: AsyncClient):
    superuser_client.follow_redirects = (
        True  # FIXME fix for starlette trailing slash redirect
    )
    response = await superuser_client.get("/api/v1/events")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == len(event_objs)


@pytest.mark.asyncio
async def test_events_all_no_superuser(user0_client: AsyncClient):
    user0_client.follow_redirects = (
        True  # FIXME fix for starlette trailing slash redirect
    )
    response = await user0_client.get("/api/v1/events")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    data = response.json()
    assert data["detail"] == "Forbidden"


@pytest.mark.asyncio
async def test_events_get_me(user0_client: AsyncClient):
    response = await user0_client.get("/api/v1/events/me")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == len(EVENTS_BY_USER_ID[AUTH_CLIENT_USER0["id"]])


@pytest.mark.asyncio
async def test_events_by_user_superuser_has_access(superuser_client: AsyncClient):
    user = AUTH_CLIENT_USER0
    response = await superuser_client.get(f"/api/v1/events/user/{user['id']}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == len(EVENTS_BY_USER_ID[AUTH_CLIENT_USER0["id"]])


@pytest.mark.asyncio
async def test_events_by_user_no_superuser_returns_forbidden(
    user3_client: AsyncClient,
):
    user = AUTH_CLIENT_USER0
    response = await user3_client.get(f"/api/v1/events/user/{user['id']}")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    data = response.json()
    assert data["detail"] == "Forbidden"


# Events calendar subrouter


@pytest.mark.asyncio
async def test_events_subrouter_get_all_events_for_calendar_by_user_with_access(
    user0_client: AsyncClient,
):
    access = AUTH_CLIENT_USER0_ACCESS_LIST[0]
    response = await user0_client.get(
        f"/api/v1/calendars/{access['calendar_id']}/events"
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == len(EVENTS_BY_CALENDAR_ID[access["calendar_id"]])


@pytest.mark.asyncio
async def test_events_subrouter_get_all_events_for_calendar_by_user_with_no_access(
    user0_client: AsyncClient,
):
    calendar = next(
        (
            calendar
            for calendar in calendar_objs
            if calendar["id"]
            not in USER_ACCESS_CALENDAR_IDS_BY_USER_ID[AUTH_CLIENT_USER0["id"]]
            and calendar["id"] not in CALENDAR_IDS_BY_USER_ID[AUTH_CLIENT_USER0["id"]]
        )
    )

    response = await user0_client.get(f"/api/v1/calendars/{calendar['id']}/events")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"].startswith("You dont have access to this calendar")


@pytest.mark.asyncio
async def test_events_subrouter_get_all_events_for_calendar_superuser(
    superuser_client: AsyncClient,
):
    calendar_id = USER_ACCESS_CALENDAR_IDS_BY_USER_ID[AUTH_CLIENT_USER0["id"]][0]
    response = await superuser_client.get(f"/api/v1/calendars/{calendar_id}/events")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == len(EVENTS_BY_CALENDAR_ID[calendar_id])


@pytest.mark.asyncio
async def test_events_subrouter_get_by_id_by_author(user0_client: AsyncClient):
    event = EVENTS_BY_USER_ID[AUTH_CLIENT_USER0["id"]][0]
    response = await user0_client.get(
        f"/api/v1/calendars/{event['calendar_id']}/events/{event['id']}"
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == event["id"]


@pytest.mark.asyncio
async def test_events_subrouter_get_by_id_by_user_with_calendar_access(
    user0_client: AsyncClient,
):
    event = next(
        (
            event
            for event in event_objs
            if event not in EVENTS_BY_USER_ID[AUTH_CLIENT_USER0["id"]]
            and event["calendar_id"]
            in USER_ACCESS_CALENDAR_IDS_BY_USER_ID[AUTH_CLIENT_USER0["id"]]
        )
    )

    response = await user0_client.get(
        f"/api/v1/calendars/{event['calendar_id']}/events/{event['id']}"
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == event["id"]


@pytest.mark.asyncio
async def test_events_subrouter_get_by_id_superuser_able_to_access(
    superuser_client: AsyncClient,
):
    event = event_objs[0]
    response = await superuser_client.get(
        f"/api/v1/calendars/{event['calendar_id']}/events/{event['id']}"
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == event["id"]


@pytest.mark.asyncio
async def test_events_subrouter_get_by_id_by_user_without_calendar_access(
    user0_client: AsyncClient,
):
    event = next(
        (
            event
            for event in event_objs
            if event not in EVENTS_BY_USER_ID[AUTH_CLIENT_USER0["id"]]
            and event["calendar_id"]
            not in USER_ACCESS_CALENDAR_IDS_BY_USER_ID[AUTH_CLIENT_USER0["id"]]
        )
    )
    response = await user0_client.get(
        f"/api/v1/calendars/{event['calendar_id']}/events/{event['id']}"
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"].startswith("You dont have access to this calendar")


@pytest.mark.asyncio
async def test_events_subrouter_create_event(user0_client: AsyncClient):
    access = AUTH_CLIENT_USER0_ACCESS_LIST[0]
    data = {
        "title": "event title",
        "description": "event description",
        "timezone": "Etc/UTC",
        "start_dt": str(pendulum.now().add(minutes=5)),
        "end_dt": str(pendulum.now().add(days=1)),
        "calendar_id": access["calendar_id"],
    }
    response = await user0_client.post(
        f"/api/v1/calendars/{access['calendar_id']}/events", json=data
    )
    print(response)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_events_subrouter_create_event_no_access_to_calendar(
    user0_client: AsyncClient,
):
    calendar = next(
        (
            calendar
            for calendar in calendar_objs
            if calendar["id"]
            not in USER_ACCESS_CALENDAR_IDS_BY_USER_ID[AUTH_CLIENT_USER0["id"]]
            and calendar["id"] not in CALENDAR_IDS_BY_USER_ID[AUTH_CLIENT_USER0["id"]]
        )
    )
    data = {
        "title": "event title no_access_to_calendar",
        "description": "event description no_access_to_calendar",
        "timezone": "Etc/UTC",
        "start_dt": str(pendulum.now().add(minutes=5)),
        "end_dt": str(pendulum.now().add(days=1)),
        "calendar_id": calendar["id"],
    }
    response = await user0_client.post(
        f"/api/v1/calendars/{calendar['id']}/events", json=data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_events_subrouter_create_event_superuser(
    superuser_client: AsyncClient,
):
    access = AUTH_CLIENT_USER1_ACCESS_LIST[0]
    data = {
        "title": "event title superuser",
        "description": "event description superuser",
        "timezone": "Etc/UTC",
        "start_dt": str(pendulum.now().add(minutes=5)),
        "end_dt": str(pendulum.now().add(days=1)),
        "calendar_id": access["calendar_id"],
    }
    response = await superuser_client.post(
        f"/api/v1/calendars/{access['calendar_id']}/events", json=data
    )
    assert response.status_code == status.HTTP_201_CREATED
    # TODO assert details


@pytest.mark.asyncio
async def test_events_subrouter_create_event_date_in_past(user0_client: AsyncClient):
    access = AUTH_CLIENT_USER0_ACCESS_LIST[0]
    data = {
        "title": "event title",
        "description": "event description",
        "timezone": "Etc/UTC",
        "start_dt": str(pendulum.now().subtract(days=1)),
        "end_dt": str(pendulum.now().subtract(days=2)),
        "calendar_id": access["calendar_id"],
    }
    response = await user0_client.post(
        f"/api/v1/calendars/{access['calendar_id']}/events", json=data
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    # TODO assert details


@pytest.mark.asyncio
async def test_events_subrouter_create_event_end_date_before_start_date(
    user0_client: AsyncClient,
):
    access = AUTH_CLIENT_USER0_ACCESS_LIST[0]
    data = {
        "title": "event title",
        "description": "event description",
        "timezone": "Etc/UTC",
        "start_dt": str(pendulum.now()),
        "end_dt": str(pendulum.now().subtract(days=2)),
        "calendar_id": access["id"],
    }
    response = await user0_client.post(
        f"/api/v1/calendars/{access['calendar_id']}/events", json=data
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    # TODO assert details


@pytest.mark.asyncio
async def test_events_subrouter_update_by_author(user0_client: AsyncClient):
    event = EVENTS_BY_USER_ID[AUTH_CLIENT_USER0["id"]][0]
    update_data = {
        "title": "updated title",
    }
    response = await user0_client.patch(
        f"/api/v1/calendars/{event['calendar_id']}/events/{event['id']}",
        json=update_data,
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_events_subrouter_update_by_user_without_calendar_access(
    user0_client: AsyncClient,
):
    calendar = next(
        (
            calendar
            for calendar in calendar_objs
            if calendar["id"]
            not in USER_ACCESS_CALENDAR_IDS_BY_USER_ID[AUTH_CLIENT_USER0["id"]]
            and calendar["id"] not in CALENDAR_IDS_BY_USER_ID[AUTH_CLIENT_USER0["id"]]
        )
    )
    event = EVENTS_BY_CALENDAR_ID[calendar["id"]][0]
    data = {"title": "updated title"}

    response = await user0_client.patch(
        f"/api/v1/calendars/{calendar['id']}/events/{event['id']}",
        json=data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"].startswith("You dont have access to this calendar")


@pytest.mark.asyncio
async def test_events_subrouter_update_by_calendar_owner(user0_client: AsyncClient):
    calendar = AUTH_CLIENT_USER0_CALENDARS[0]
    event = EVENTS_BY_CALENDAR_ID[calendar["id"]][0]
    data = {"title": "updated title"}

    response = await user0_client.patch(
        f"/api/v1/calendars/{calendar['id']}/events/{event['id']}", json=data
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_events_subrouter_update_by_calendar_moderator(user3_client: AsyncClient):
    access = next(
        (
            access
            for access in calendar_access_objs
            if access["user_id"] == AUTH_CLIENT_USER3["id"]
            and access["role"] == CalendarAccessRole.MODERATOR.value
        )
    )
    event = next(
        (
            event
            for event in EVENTS_BY_CALENDAR_ID[access["calendar_id"]]
            if event["created_by"] != AUTH_CLIENT_USER3["id"]
        )
    )
    data = {"title": "updated by moderator"}

    response = await user3_client.patch(
        f"/api/v1/calendars/{access['calendar_id']}/events/{event['id']}", json=data
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_events_subrouter_update_by_calendar_standard(
    user3_client: AsyncClient,
):
    access = next(
        (
            access
            for access in calendar_access_objs
            if access["user_id"] == AUTH_CLIENT_USER3["id"]
            and access["role"] == CalendarAccessRole.STANDARD.value
        )
    )
    event = next(
        (
            event
            for event in EVENTS_BY_CALENDAR_ID[access["calendar_id"]]
            if event["created_by"] != AUTH_CLIENT_USER3["id"]
        )
    )
    data = {"title": "updated by standard"}

    response = await user3_client.patch(
        f"/api/v1/calendars/{access['calendar_id']}/events/{event['id']}", json=data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "Unauthorized"


@pytest.mark.asyncio
async def test_events_subrouter_update_by_calendar_guest(
    user1_client: AsyncClient,
):
    access = next(
        (
            access
            for access in calendar_access_objs
            if access["user_id"] == AUTH_CLIENT_USER1["id"]
            and access["role"] == CalendarAccessRole.GUEST.value
        )
    )
    event = next(
        (
            event
            for event in EVENTS_BY_CALENDAR_ID[access["calendar_id"]]
            if event["created_by"] != AUTH_CLIENT_USER1["id"]
        )
    )
    data = {"title": "updated by guest"}

    response = await user1_client.patch(
        f"/api/v1/calendars/{access['calendar_id']}/events/{event['id']}", json=data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "Unauthorized"


@pytest.mark.asyncio
async def test_events_subrouter_delete_by_author(user0_client: AsyncClient):
    event = EVENTS_BY_USER_ID[AUTH_CLIENT_USER0["id"]][0]
    reponse = await user0_client.delete(
        f"/api/v1/calendars/{event['calendar_id']}/events/{event['id']}"
    )
    assert reponse.status_code == status.HTTP_204_NO_CONTENT

    check = await user0_client.get(
        f"/api/v1/calendars/{event['calendar_id']}/events/{event['id']}"
    )
    assert check.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_events_subrouter_delete_by_user_without_calendar_access(
    user0_client: AsyncClient,
):
    access = next(
        (
            access
            for access in calendar_access_objs
            if access["calendar_id"] not in AUTH_CLIENT_USER0_ACCESS_LIST
        )
    )
    event = EVENTS_BY_CALENDAR_ID[access["calendar_id"]][0]
    response = await user0_client.delete(
        f"/api/v1/calendars/{event['calendar_id']}/events/{event['id']}"
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_events_subrouter_delete_by_calendar_owner(user0_client: AsyncClient):
    calendar = AUTH_CLIENT_USER0_CALENDARS[0]
    event = next(
        (
            event
            for event in EVENTS_BY_CALENDAR_ID[calendar["id"]]
            if event["created_by"] != AUTH_CLIENT_USER0["id"]
        )
    )
    reponse = await user0_client.delete(
        f"/api/v1/calendars/{event['calendar_id']}/events/{event['id']}"
    )
    assert reponse.status_code == status.HTTP_204_NO_CONTENT

    check = await user0_client.get(
        f"/api/v1/calendars/{event['calendar_id']}/events/{event['id']}"
    )
    assert check.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_events_subrouter_delete_by_calendar_moderator(user3_client: AsyncClient):
    access = next(
        (
            access
            for access in calendar_access_objs
            if access["user_id"] == AUTH_CLIENT_USER3["id"]
            and access["role"] == CalendarAccessRole.MODERATOR.value
        )
    )
    event = next(
        (
            event
            for event in EVENTS_BY_CALENDAR_ID[access["calendar_id"]]
            if event["created_by"] != AUTH_CLIENT_USER3["id"]
        )
    )

    response = await user3_client.delete(
        f"/api/v1/calendars/{access['calendar_id']}/events/{event['id']}"
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_events_subrouter_delete_by_calendar_standard(
    user3_client: AsyncClient,
):
    access = next(
        (
            access
            for access in calendar_access_objs
            if access["user_id"] == AUTH_CLIENT_USER3["id"]
            and access["role"] == CalendarAccessRole.STANDARD.value
        )
    )
    event = next(
        (
            event
            for event in EVENTS_BY_CALENDAR_ID[access["calendar_id"]]
            if event["created_by"] != AUTH_CLIENT_USER3["id"]
        )
    )

    response = await user3_client.delete(
        f"/api/v1/calendars/{access['calendar_id']}/events/{event['id']}"
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "Unauthorized"


@pytest.mark.asyncio
async def test_events_subrouter_delete_by_calendar_guest(
    user1_client: AsyncClient,
):
    access = next(
        (
            access
            for access in calendar_access_objs
            if access["user_id"] == AUTH_CLIENT_USER1["id"]
            and access["role"] == CalendarAccessRole.GUEST.value
        )
    )
    event = next(
        (
            event
            for event in EVENTS_BY_CALENDAR_ID[access["calendar_id"]]
            if event["created_by"] != AUTH_CLIENT_USER1["id"]
        )
    )

    response = await user1_client.delete(
        f"/api/v1/calendars/{access['calendar_id']}/events/{event['id']}"
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "Unauthorized"
