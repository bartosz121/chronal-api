import uuid

import pytest
from httpx import AsyncClient

from chronal_api.calendar_access.models import CalendarAccessRole

from .data import (
    AUTH_CLIENT_USER0,
    AUTH_CLIENT_USER0_CALENDARS,
    AUTH_CLIENT_USER1,
    AUTH_CLIENT_USER2,
    AUTH_CLIENT_USER2_CALENDARS,
    AUTH_CLIENT_USER3,
    calendar_access_objs,
    calendar_objs,
)


@pytest.mark.asyncio
async def test_calendars_list_superuser(superuser_client: AsyncClient):
    superuser_client.follow_redirects = (
        True  # FIXME fix for starlette trailing slash redirect
    )
    response = await superuser_client.get("/api/v1/calendars")
    assert response.status_code == 200
    assert len(response.json()) == len(calendar_objs)


@pytest.mark.asyncio
async def test_calendars_list_no_superuser_returns_403(user0_client: AsyncClient):
    user0_client.follow_redirects = (
        True  # FIXME fix for starlette trailing slash redirect
    )
    response = await user0_client.get("/api/v1/calendars")
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"


@pytest.mark.asyncio
async def test_calendars_create_no_auth_unauthorized(client: AsyncClient):
    client.follow_redirects = True  # FIXME fix for starlette trailing slash redirect
    data = {
        "name": "My Calendar #1",
        "description": "My calendar description",
    }

    response = await client.post("/api/v1/calendars", json=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


@pytest.mark.asyncio
async def test_calendars_create(user0_client: AsyncClient):
    user0_client.follow_redirects = (
        True  # FIXME fix for starlette trailing slash redirect
    )
    data = {
        "name": "My Calendar #1",
        "description": "My calendar description",
    }

    response = await user0_client.post("/api/v1/calendars", json=data)

    assert response.status_code == 201
    url_created = response.json()["resource_url"]

    response_check = await user0_client.get(url_created)
    data_created = response_check.json()
    assert data_created["name"] == data["name"]
    assert data_created["description"] == data["description"]


@pytest.mark.asyncio
async def test_calendars_create_returns_validation_error(user0_client: AsyncClient):
    user0_client.follow_redirects = (
        True  # FIXME fix for starlette trailing slash redirect
    )
    data = {
        "description": "No name",
    }

    response = await user0_client.post("/api/v1/calendars", json=data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_calendars_me(user0_client: AsyncClient):
    response = await user0_client.get("/api/v1/calendars/me")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == len(AUTH_CLIENT_USER0_CALENDARS)
    assert all((calendar["owner_id"] == AUTH_CLIENT_USER0["id"] for calendar in data))


@pytest.mark.asyncio
async def test_calendars_by_id(user0_client: AsyncClient):
    calendar = AUTH_CLIENT_USER0_CALENDARS[-1]

    response = await user0_client.get(f"/api/v1/calendars/{calendar['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == calendar["id"]


@pytest.mark.asyncio
async def test_calendars_by_id_returns_not_found(user0_client: AsyncClient):
    response = await user0_client.get(f"/api/v1/calendars/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


@pytest.mark.asyncio
async def test_calendars_by_id_not_owner_returns_unauthorized(
    user0_client: AsyncClient,
):
    calendar = AUTH_CLIENT_USER2_CALENDARS[-1]

    response = await user0_client.get(f"/api/v1/calendars/{calendar['id']}")
    assert response.status_code == 401
    assert response.json()["detail"].startswith("You dont have access to this calendar")


@pytest.mark.asyncio
async def test_calendars_patch(user0_client: AsyncClient):
    calendar = AUTH_CLIENT_USER0_CALENDARS[0]

    patch_data = {
        "name": "patched name",
        "description": "patched description",
    }

    response = await user0_client.patch(
        f"/api/v1/calendars/{calendar['id']}", json=patch_data
    )
    assert response.status_code == 200
    url_patched = response.json()["resource_url"]

    response_check = await user0_client.get(url_patched)
    patched_data = response_check.json()
    assert patched_data["name"] == patch_data["name"]
    assert patched_data["description"] == patch_data["description"]


@pytest.mark.asyncio
async def test_calendars_patch_no_access_returns_unauthorized(
    user0_client: AsyncClient,
):
    calendar = AUTH_CLIENT_USER2_CALENDARS[-1]

    patch_data = {
        "name": "patched name",
        "description": "patched description",
    }

    response = await user0_client.patch(
        f"/api/v1/calendars/{calendar['id']}", json=patch_data
    )
    assert response.status_code == 401
    assert response.json()["detail"].startswith("You dont have access to this calendar")


@pytest.mark.asyncio
async def test_get_calendar_access_list_owner(user0_client: AsyncClient):
    calendar = AUTH_CLIENT_USER0_CALENDARS[-1]
    calendar_access_len = (
        len(
            tuple(
                access
                for access in calendar_access_objs
                if access["calendar_id"] == calendar["id"]
            )
        )
        + 1
    )  # +1 for owner access created in `add_data` function via sqlalchemy event

    response = await user0_client.get(f"/api/v1/calendars/{calendar['id']}/access")

    assert response.status_code == 200
    assert len(response.json()) == calendar_access_len


@pytest.mark.asyncio
async def test_get_calendar_access_list_standard_access(user2_client: AsyncClient):
    calendar = AUTH_CLIENT_USER0_CALENDARS[0]
    calendar_access_len = (
        len(
            tuple(
                access
                for access in calendar_access_objs
                if access["calendar_id"] == calendar["id"]
            )
        )
        + 1
    )  # +1 for owner access created in `add_data` function via sqlalchemy event

    response = await user2_client.get(f"/api/v1/calendars/{calendar['id']}/access")

    assert response.status_code == 200
    assert len(response.json()) == calendar_access_len


@pytest.mark.asyncio
async def test_get_calendar_access_list_no_access_returns_unauthorized(
    user0_client: AsyncClient,
):
    calendar = AUTH_CLIENT_USER2_CALENDARS[-1]

    response = await user0_client.get(f"/api/v1/calendars/{calendar['id']}/access")

    assert response.status_code == 401
    assert response.json()["detail"].startswith("You dont have access to this calendar")


@pytest.mark.asyncio
async def test_get_calendar_access_list_superuser_is_allowed(
    superuser_client: AsyncClient,
):
    calendar = AUTH_CLIENT_USER0_CALENDARS[-1]

    calendar_access_len = (
        len(
            tuple(
                access
                for access in calendar_access_objs
                if access["calendar_id"] == calendar["id"]
            )
        )
        + 1
    )  # +1 for owner access created in `add_data` function via sqlalchemy event

    response = await superuser_client.get(f"/api/v1/calendars/{calendar['id']}/access")

    assert response.status_code == 200
    assert len(response.json()) == calendar_access_len


@pytest.mark.asyncio
async def test_create_calendar_access_by_owner(user0_client: AsyncClient):
    calendar = AUTH_CLIENT_USER0_CALENDARS[1]
    data = {
        "user_id": AUTH_CLIENT_USER3["id"],
        "role": CalendarAccessRole.STANDARD.value,
    }

    response = await user0_client.post(
        f"/api/v1/calendars/{calendar['id']}/access", json=data
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_calendar_access_by_owner_returns_bad_request_if_user_does_not_exist(
    user0_client: AsyncClient,
):
    calendar = AUTH_CLIENT_USER0_CALENDARS[1]
    data = {
        "user_id": str(uuid.uuid4()),
        "role": CalendarAccessRole.STANDARD.value,
    }

    response = await user0_client.post(
        f"/api/v1/calendars/{calendar['id']}/access", json=data
    )
    assert response.status_code == 400
    detail = response.json()["detail"]
    assert detail.endswith("does not exist")


@pytest.mark.asyncio
async def test_create_calendar_access_owner_returns_already_has_access(
    user0_client: AsyncClient,
):
    calendar = AUTH_CLIENT_USER0_CALENDARS[2]
    data = {
        "user_id": AUTH_CLIENT_USER2["id"],
        "role": CalendarAccessRole.STANDARD.value,
    }

    response_1 = await user0_client.post(
        f"/api/v1/calendars/{calendar['id']}/access", json=data
    )
    assert response_1.status_code == 201

    response_2 = await user0_client.post(
        f"/api/v1/calendars/{calendar['id']}/access", json=data
    )
    assert response_2.status_code == 400
    assert "already has access to this calendar" in response_2.json()["detail"]


@pytest.mark.asyncio
async def test_create_calendar_access_superuser_able_to_create(
    superuser_client: AsyncClient,
):
    calendar = AUTH_CLIENT_USER2_CALENDARS[0]
    data = {
        "user_id": AUTH_CLIENT_USER1["id"],
        "role": CalendarAccessRole.STANDARD.value,
    }

    response = await superuser_client.post(
        f"/api/v1/calendars/{calendar['id']}/access", json=data
    )

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_calendar_access_has_access_but_not_owner_returns_unauthorized(
    user2_client: AsyncClient,
):
    calendar = AUTH_CLIENT_USER0_CALENDARS[1]

    data = {
        "user_id": AUTH_CLIENT_USER3,
        "role": CalendarAccessRole.STANDARD.value,
    }
    response = await user2_client.post(
        f"/api/v1/calendars/{calendar['id']}/access", json=data
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "You don't have sufficient access"


@pytest.mark.asyncio
async def test_calendars_delete(user0_client: AsyncClient):
    calendar = AUTH_CLIENT_USER0_CALENDARS[0]

    response = await user0_client.delete(f"/api/v1/calendars/{calendar['id']}")
    assert response.status_code == 204

    response_check_if_removed = await user0_client.get(
        f"/api/v1/calendars/{calendar['id']}"
    )
    assert response_check_if_removed.status_code == 404


@pytest.mark.asyncio
async def test_calendars_delete_not_owner_returns_unauthorized(
    user0_client: AsyncClient,
):
    calendar = AUTH_CLIENT_USER2_CALENDARS[-1]

    response = await user0_client.delete(f"/api/v1/calendars/{calendar['id']}")
    assert response.status_code == 401
    assert response.json()["detail"].startswith("You dont have access to this calendar")


@pytest.mark.asyncio
async def test_calendars_delete_superuser_able_to_delete_others(
    superuser_client: AsyncClient,
):
    calendar = AUTH_CLIENT_USER2_CALENDARS[-1]

    response = await superuser_client.delete(f"/api/v1/calendars/{calendar['id']}")
    assert response.status_code == 204

    response_check_if_removed = await superuser_client.get(
        f"/api/v1/calendars/{calendar['id']}"
    )
    assert response_check_if_removed.status_code == 404
