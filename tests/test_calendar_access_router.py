import uuid

import pytest
from httpx import AsyncClient

from chronal_api.calendar_access.models import CalendarAccessRole

from .data import (
    AUTH_CLIENT_USER0,
    AUTH_CLIENT_USER0_ACCESS_CREATED_BY,
    AUTH_CLIENT_USER0_ACCESS_LIST,
    AUTH_CLIENT_USER0_CALENDARS,
    AUTH_CLIENT_USER1,
    AUTH_CLIENT_USER1_ACCESS_CREATED_BY,
    AUTH_CLIENT_USER1_ACCESS_LIST,
    AUTH_CLIENT_USER2,
    AUTH_CLIENT_USER2_ACCESS_LIST,
    AUTH_CLIENT_USER3,
    AUTH_CLIENT_USER3_ACCESS_LIST,
    AUTH_CLIENT_USER4_ACCESS_LIST,
    AUTH_CLIENT_USER5_ACCESS_LIST,
    calendar_access_objs,
    calendar_objs,
)


@pytest.mark.asyncio
async def test_calendars_access_list_superuser(superuser_client: AsyncClient):
    superuser_client.follow_redirects = (
        True  # FIXME fix for starlette trailing slash redirect
    )
    response = await superuser_client.get(f"/api/v1/calendars-access")
    assert response.status_code == 200
    assert len(response.json()) == len(calendar_access_objs) + len(calendar_objs)


@pytest.mark.asyncio
async def test_calendars_access_list_no_superuser_returns_403(
    user0_client: AsyncClient,
):
    user0_client.follow_redirects = (
        True  # FIXME fix for starlette trailing slash redirect
    )
    response = await user0_client.get(f"/api/v1/calendars-access")
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"


@pytest.mark.asyncio
async def test_calendars_access_me(user0_client: AsyncClient):
    user0_access_len = len(AUTH_CLIENT_USER0_CALENDARS) + len(
        AUTH_CLIENT_USER0_ACCESS_LIST
    )

    response = await user0_client.get("/api/v1/calendars-access/me")
    assert response.status_code == 200
    assert len(response.json()) == user0_access_len


@pytest.mark.asyncio
async def test_calendars_access_me_superuser_access_all(superuser_client: AsyncClient):
    user0_access_len = len(AUTH_CLIENT_USER0_CALENDARS) + len(
        AUTH_CLIENT_USER0_ACCESS_LIST
    )

    response = await superuser_client.get(
        f"/api/v1/calendars-access/user/{AUTH_CLIENT_USER0['id']}"
    )
    assert response.status_code == 200
    assert len(response.json()) == user0_access_len


@pytest.mark.asyncio
async def test_calendars_access_by_id(user0_client: AsyncClient):
    access = AUTH_CLIENT_USER0_ACCESS_LIST[0]
    response = await user0_client.get(f"/api/v1/calendars-access/{access['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == access["id"]


@pytest.mark.asyncio
async def test_calendars_access_by_id_not_owner_returns_unauthorized(
    user2_client: AsyncClient,
):
    access = AUTH_CLIENT_USER0_ACCESS_LIST[0]
    response = await user2_client.get(f"/api/v1/calendars-access/{access['id']}")
    assert response.status_code == 401
    assert response.json()["detail"] == "You don't have access to this resource"


@pytest.mark.asyncio
async def test_calendars_access_by_id_superuser_can_access(
    superuser_client: AsyncClient,
):
    access = AUTH_CLIENT_USER0_ACCESS_LIST[0]
    response = await superuser_client.get(f"/api/v1/calendars-access/{access['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == access["id"]


@pytest.mark.asyncio
async def test_calendars_access_by_id_wrong_id_not_found(user0_client: AsyncClient):
    response = await user0_client.get(f"/api/v1/calendars-access/{str(uuid.uuid4())}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


@pytest.mark.asyncio
async def test_calendars_access_delete_owner_able_to_delete(user0_client: AsyncClient):
    access = AUTH_CLIENT_USER0_ACCESS_CREATED_BY[-1]
    response = await user0_client.delete(
        f"/api/v1/calendars-access/{access['calendar_id']}/{access['id']}"
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_calendars_access_delete_no_access_returns_unauthorized(
    user2_client: AsyncClient,
):
    access = AUTH_CLIENT_USER0_ACCESS_CREATED_BY[0]
    response = await user2_client.delete(
        f"/api/v1/calendars-access/{access['calendar_id']}/{access['id']}"
    )

    assert response.status_code == 401

    detail = response.json()["detail"]
    assert detail == "Unauthorized"


@pytest.mark.asyncio
async def test_calendars_access_delete_with_access_but_not_owner_returns_unauthorized(
    user2_client: AsyncClient,
):
    access = AUTH_CLIENT_USER0_ACCESS_CREATED_BY[3]
    response = await user2_client.delete(
        f"/api/v1/calendars-access/{access['calendar_id']}/{access['id']}"
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_calendars_access_delete_superuser_can_delete(
    superuser_client: AsyncClient,
):
    access = AUTH_CLIENT_USER1_ACCESS_CREATED_BY[0]
    response = await superuser_client.delete(
        f"/api/v1/calendars-access/{access['calendar_id']}/{access['id']}"
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_calendars_access_delete_wrong_calendar_id_returns_404(
    user0_client: AsyncClient,
):
    access = AUTH_CLIENT_USER0_ACCESS_CREATED_BY[0]
    response = await user0_client.delete(
        f"/api/v1/calendars-access/{str(uuid.uuid4())}/{access['id']}"
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_calendars_access_delete_wrong_calendar_access_id_returns_404(
    user0_client: AsyncClient,
):
    access = AUTH_CLIENT_USER0_ACCESS_CREATED_BY[0]
    response = await user0_client.delete(
        f"/api/v1/calendars-access/{access['calendar_id']}/{str(uuid.uuid4())}"
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_calendars_access_delete_user_is_able_to_delete_his_own_access(
    user2_client: AsyncClient,
):
    access = AUTH_CLIENT_USER2_ACCESS_LIST
    response = await user2_client.delete(
        f"/api/v1/calendars-access/{access[2]['calendar_id']}/{access[2]['id']}"
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_calendars_access_delete_owner_not_able_to_remove_his_own_owner_access(
    user4_client: AsyncClient,
):
    access_list = (await user4_client.get("/api/v1/calendars-access/me")).json()

    response = await user4_client.delete(
        f"/api/v1/calendars-access/{access_list[0]['calendar_id']}/{access_list[0]['id']}"
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Owner cannot remove his access"


@pytest.mark.asyncio
async def test_calendars_access_delete_guest_able_to_delete_himself(
    user1_client: AsyncClient,
):
    access = AUTH_CLIENT_USER1_ACCESS_LIST[0]
    response = await user1_client.delete(
        f"/api/v1/calendars-access/{access['calendar_id']}/{access['id']}"
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_calendars_access_delete_guest_user_not_able_to_delete_others(
    user1_client: AsyncClient,
):
    access = AUTH_CLIENT_USER2_ACCESS_LIST[0]
    print(access)
    response = await user1_client.delete(
        f"/api/v1/calendars-access/{access['calendar_id']}/{access['id']}"
    )
    assert response.status_code == 401

    detail = response.json()["detail"]
    assert detail == "Unauthorized"


@pytest.mark.asyncio
async def test_calendars_access_delete_standard_user_able_to_delete_himself(
    user2_client: AsyncClient,
):
    access = AUTH_CLIENT_USER2_ACCESS_LIST[0]
    response = await user2_client.delete(
        f"/api/v1/calendars-access/{access['calendar_id']}/{access['id']}"
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_calendars_access_delete_standard_user_not_able_to_delete_others(
    user2_client: AsyncClient,
):
    access = AUTH_CLIENT_USER1_ACCESS_LIST[0]
    response = await user2_client.delete(
        f"/api/v1/calendars-access/{access['calendar_id']}/{access['id']}"
    )
    assert response.status_code == 401

    detail = response.json()["detail"]
    assert detail == "Unauthorized"


@pytest.mark.asyncio
async def test_calendars_access_delete_moderator_able_to_delete_himself(
    user3_client: AsyncClient,
):
    access = AUTH_CLIENT_USER3_ACCESS_LIST[0]
    response = await user3_client.delete(
        f"/api/v1/calendars-access/{access['calendar_id']}/{access['id']}"
    )
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_calendars_access_delete_moderator_able_to_delete_standard_and_guests(
    user3_client: AsyncClient,
):
    access_guest = AUTH_CLIENT_USER1_ACCESS_LIST[0]
    response_guest = await user3_client.delete(
        f"/api/v1/calendars-access/{access_guest['calendar_id']}/{access_guest['id']}"
    )
    assert response_guest.status_code == 204

    access_standard = AUTH_CLIENT_USER2_ACCESS_LIST[0]
    response_standard = await user3_client.delete(
        f"/api/v1/calendars-access/{access_standard['calendar_id']}/{access_standard['id']}"
    )
    assert response_standard.status_code == 204


@pytest.mark.asyncio
async def test_calendars_access_delete_moderator_not_able_to_delete_moderators_and_owners(
    user3_client: AsyncClient,
):
    access_moderator = AUTH_CLIENT_USER5_ACCESS_LIST[0]
    response_moderator = await user3_client.delete(
        f"/api/v1/calendars-access/{access_moderator['calendar_id']}/{access_moderator['id']}"
    )
    assert response_moderator.status_code == 401

    access_owner = tuple(
        filter(
            lambda x: x["role"] == CalendarAccessRole.OWNER.value,
            (
                await user3_client.get(
                    f"/api/v1/calendars/{AUTH_CLIENT_USER3_ACCESS_LIST[0]['calendar_id']}/access"
                )
            ).json(),
        )
    )[0]

    response_owner = await user3_client.delete(
        f"/api/v1/calendars-access/{access_owner['calendar_id']}/{access_owner['id']}"
    )
    assert response_owner.status_code == 401
