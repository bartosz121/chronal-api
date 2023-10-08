from uuid import uuid4

import httpx
from faker import Faker
from fastapi import status

from chronal_api.calendars import exceptions as calendars_exceptions
from chronal_api.calendars import schemas as calendars_schemas
from chronal_api.lib.auth import models as auth_models
from tests import factories

fake = Faker()


async def test_list_users_calendars(
    calendar_factory: factories.CalendarFactory,
    authorized_client: tuple[httpx.AsyncClient, auth_models.AccessToken],
):
    client, token = authorized_client
    calendars = await calendar_factory.create_batch(10, owner=token.user)

    response = await client.get("/calendars")
    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert len(response_json) == len(calendars)
    assert all(calendar["id"] in [str(cal.id) for cal in calendars] for calendar in response_json)


async def test_list_users_calendars_unauthorized_401(client: httpx.AsyncClient):
    response = await client.get("/calendars")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_list_users_calendars_empty(
    authorized_client: tuple[httpx.AsyncClient, auth_models.AccessToken],
):
    client, _ = authorized_client
    response = await client.get("/calendars")
    assert response.status_code == status.HTTP_200_OK

    assert response.json() == []


async def test_get_by_id(
    calendar_factory: factories.CalendarFactory,
    authorized_client: tuple[httpx.AsyncClient, auth_models.AccessToken],
):
    client, token = authorized_client
    cal = await calendar_factory.create(owner=token.user)

    response = await client.get(f"/calendars/{str(cal.id)}")
    assert response.status_code == status.HTTP_200_OK

    expected_response = calendars_schemas.CalendarRead.model_validate(cal)
    response_json = response.json()

    assert response_json["id"] == str(expected_response.id)
    del response_json["id"]

    assert response_json == expected_response.model_dump(exclude={"id"})


async def test_get_by_id_unauthorized_401(client: httpx.AsyncClient):
    response = await client.get(f"/calendars/{str(uuid4())}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"]["msg"] == "Unauthorized"


async def test_get_by_id_forbidden_403(
    calendar_factory: factories.CalendarFactory,
    authorized_client: tuple[httpx.AsyncClient, auth_models.AccessToken],
):
    client, _ = authorized_client
    cal = await calendar_factory.create()

    response = await client.get(f"/calendars/{str(cal.id)}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"]["msg"] == calendars_exceptions.HTTPError.FORBIDDEN


async def test_get_by_id_not_found_404(
    authorized_client: tuple[httpx.AsyncClient, auth_models.AccessToken],
):
    client, _ = authorized_client
    response = await client.get(f"/calendars/{str(uuid4())}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"]["msg"] == calendars_exceptions.HTTPError.CALENDAR_NOT_FOUND


async def test_create(
    authorized_client: tuple[httpx.AsyncClient, auth_models.AccessToken],
):
    client, _ = authorized_client
    data = calendars_schemas.CalendarCreate(
        title=fake.text(max_nb_chars=32), description=fake.text(max_nb_chars=120)
    )
    response = await client.post("/calendars", json=data.model_dump())
    assert response.status_code == status.HTTP_201_CREATED

    response_json = response.json()

    assert response_json["id"]
    assert response_json["title"] == data.title
    assert response_json["description"] == data.description


async def test_create_unauthorized_401(client: httpx.AsyncClient):
    data = calendars_schemas.CalendarCreate(
        title=fake.text(max_nb_chars=32), description=fake.text(max_nb_chars=120)
    )
    response = await client.post("/calendars", json=data.model_dump())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_create_title_not_unique_409(
    calendar_factory: factories.CalendarFactory,
    authorized_client: tuple[httpx.AsyncClient, auth_models.AccessToken],
):
    client, token = authorized_client
    calendar_1 = await calendar_factory.create(owner=token.user)
    data = calendars_schemas.CalendarCreate(
        title=calendar_1.title, description=fake.text(max_nb_chars=120)
    )

    response = await client.post("/calendars", json=data.model_dump())
    assert response.status_code == status.HTTP_409_CONFLICT

    response_json = response.json()
    assert response_json["detail"]["msg"] == calendars_exceptions.HTTPError.TITLE_NOT_UNIQUE


async def test_update(
    calendar_factory: factories.CalendarFactory,
    authorized_client: tuple[httpx.AsyncClient, auth_models.AccessToken],
):
    TITLE = "title updated"

    client, token = authorized_client
    cal = await calendar_factory.create(owner=token.user)
    data = calendars_schemas.CalendarPatch(title=TITLE)

    response = await client.patch(f"/calendars/{str(cal.id)}", json=data.model_dump())
    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    assert response_json["id"] == str(cal.id)
    assert response_json["title"] == TITLE
    assert response_json["description"] == cal.description


async def test_update_unauthorized_401(client: httpx.AsyncClient):
    response = await client.patch(f"/calendars/{str(uuid4())}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"]["msg"] == "Unauthorized"


async def test_update_forbidden_403(
    calendar_factory: factories.CalendarFactory,
    authorized_client: tuple[httpx.AsyncClient, auth_models.AccessToken],
):
    client, _ = authorized_client
    cal = await calendar_factory.create()
    data = calendars_schemas.CalendarPatch(title="title123")

    response = await client.patch(f"/calendars/{str(cal.id)}", json=data.model_dump())
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"]["msg"] == calendars_exceptions.HTTPError.FORBIDDEN


async def test_update_not_found_404(
    authorized_client: tuple[httpx.AsyncClient, auth_models.AccessToken],
):
    client, _ = authorized_client
    response = await client.patch(f"/calendars/{str(uuid4())}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"]["msg"] == calendars_exceptions.HTTPError.CALENDAR_NOT_FOUND


async def test_update_title_not_unique_409(
    calendar_factory: factories.CalendarFactory,
    authorized_client: tuple[httpx.AsyncClient, auth_models.AccessToken],
):
    client, token = authorized_client
    cal_1 = await calendar_factory.create(owner=token.user)
    cal_2 = await calendar_factory.create(owner=token.user)
    data = calendars_schemas.CalendarPatch(title=cal_1.title)

    response = await client.patch(f"/calendars/{str(cal_2.id)}", json=data.model_dump())
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"]["msg"] == calendars_exceptions.HTTPError.TITLE_NOT_UNIQUE


async def test_delete(
    calendar_factory: factories.CalendarFactory,
    authorized_client: tuple[httpx.AsyncClient, auth_models.AccessToken],
):
    client, token = authorized_client
    cal = await calendar_factory.create(owner=token.user)

    response = await client.delete(f"/calendars/{str(cal.id)}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_delete_unauthorized_401(client: httpx.AsyncClient):
    response = await client.delete(f"/calendars/{str(uuid4())}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"]["msg"] == "Unauthorized"


async def test_delete_forbidden_403(
    calendar_factory: factories.CalendarFactory,
    authorized_client: tuple[httpx.AsyncClient, auth_models.AccessToken],
):
    client, _ = authorized_client
    cal = await calendar_factory.create()

    response = await client.delete(f"/calendars/{str(cal.id)}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"]["msg"] == calendars_exceptions.HTTPError.FORBIDDEN


async def test_delete_not_found_404(
    authorized_client: tuple[httpx.AsyncClient, auth_models.AccessToken],
):
    client, _ = authorized_client

    response = await client.delete(f"/calendars/{str(uuid4())}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"]["msg"] == calendars_exceptions.HTTPError.CALENDAR_NOT_FOUND
