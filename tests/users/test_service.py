from unittest import mock

import pytest

from chronal_api.users import exceptions as users_exceptions
from chronal_api.users import schemas as users_schemas
from chronal_api.users import service as users_service


@pytest.fixture
def user_service() -> users_service.UserService:
    return users_service.UserService(mock.AsyncMock())


def test_user_repository_init():
    repository = mock.Mock()

    service = users_service.UserService(repository)
    assert service.repository == repository


@mock.patch("chronal_api.lib.auth.security.get_password_hash")
async def test_create_user(
    mock_get_password_hash: mock.MagicMock, user_service: users_service.UserService
):
    mock_get_password_hash.return_value = "password"
    user_service.repository.email_exists.return_value = False
    user_service.repository.create_user.return_value = mock.Mock()
    schema = users_schemas.UserCreate(email="example@example.com", password="passw0rd123!@#")

    r = await user_service.create_user(schema)

    mock_get_password_hash.assert_called_once_with(schema.password)
    user_service.repository.email_exists.assert_called_once_with(schema.email)
    user_service.repository.create_user.assert_called_once_with(
        schema.email, mock_get_password_hash.return_value
    )
    assert r


@mock.patch("chronal_api.lib.auth.security.get_password_hash")
async def test_create_user_raises_email_already_exists(
    mock_get_password_hash: mock.MagicMock, user_service: users_service.UserService
):
    mock_get_password_hash.return_value = "password"
    user_service.repository.email_exists.return_value = True
    schema = users_schemas.UserCreate(email="example@example.com", password="passw0rd123!@#")

    with pytest.raises(users_exceptions.EmailAlreadyExists):
        await user_service.create_user(schema)


async def test_get_by_email(user_service: users_service.UserService):
    user_service.repository.get_by_email.return_value = mock.Mock()
    r = await user_service.get_by_email("email")
    user_service.repository.get_by_email.assert_called_once_with("email")
    assert r == user_service.repository.get_by_email.return_value


async def test_get_by_email_raises_user_not_founnd(user_service: users_service.UserService):
    user_service.repository.get_by_email.return_value = None
    with pytest.raises(users_exceptions.UserNotFound):
        await user_service.get_by_email("email")
