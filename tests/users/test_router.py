import uuid
from typing import TYPE_CHECKING

from faker import Faker
from fastapi import status
from sqlalchemy import select

from chronal_api.lib.auth import models as auth_models
from chronal_api.users import exceptions as users_exceptions
from chronal_api.users import schemas as users_schemas
from tests import factories

if TYPE_CHECKING:
    import httpx
    from sqlalchemy.ext.asyncio import AsyncSession


faker = Faker()


async def test_register(client: "httpx.AsyncClient"):
    data = users_schemas.UserCreate(
        email=faker.email(), password=factories.UserFactory._DEFAULT_PASSWORD
    )

    response = await client.post("/users/register", json=data.model_dump())
    assert response.status_code == status.HTTP_201_CREATED

    response_json = response.json()
    assert response_json["id"]
    assert uuid.UUID(response_json["id"])
    assert response_json["email"] == data.email


async def test_register_409_email_already_exists(
    client: "httpx.AsyncClient", user_factory: factories.UserFactory
):
    user = await user_factory.create()

    data = users_schemas.UserCreate(
        email=user.email, password=factories.UserFactory._DEFAULT_PASSWORD
    )

    response = await client.post("/users/register", json=data.model_dump())
    assert response.status_code == status.HTTP_409_CONFLICT

    response_json = response.json()
    assert response_json["detail"]["msg"] == users_exceptions.HTTPError.EMAIL_ALREADY_IN_USE


async def test_token(client: "httpx.AsyncClient", user_factory: factories.UserFactory):
    user = await user_factory.create()

    data = users_schemas.CreateToken(
        email=user.email, password=factories.UserFactory._DEFAULT_PASSWORD
    )

    response = await client.post("/users/token", json=data.model_dump())
    assert response.status_code == status.HTTP_201_CREATED


async def test_token_404_user_with_email_does_not_exist(client: "httpx.AsyncClient"):
    data = users_schemas.CreateToken(email="abc@abc.com", password="password")

    response = await client.post("/users/token", json=data.model_dump())
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response_json = response.json()
    assert response_json["detail"]["msg"] == users_exceptions.HTTPError.EMAIL_NOT_FOUND


async def test_token_400_wrong_password(
    client: "httpx.AsyncClient", user_factory: factories.UserFactory
):
    user = await user_factory.create()

    data = users_schemas.CreateToken(email=user.email, password="wrong_password")

    response = await client.post("/users/token", json=data.model_dump())
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_json = response.json()
    assert response_json["detail"]["msg"] == users_exceptions.HTTPError.WRONG_PASSWORD


async def test_logout(
    authorized_client: tuple["httpx.AsyncClient", auth_models.AccessToken],
    session: "AsyncSession",
):
    client, token = authorized_client

    response = await client.get("/users/logout")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    token_in_db = (
        await session.execute(
            select(auth_models.AccessToken).where(
                auth_models.AccessToken.access_token == token.access_token
            )
        )
    ).scalar_one_or_none()
    assert token_in_db is None


async def test_logout_204_not_authenticated(client: "httpx.AsyncClient"):
    response = await client.get("/users/logout")
    assert response.status_code == status.HTTP_204_NO_CONTENT
