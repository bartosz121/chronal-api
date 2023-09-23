from datetime import datetime, timezone
from unittest import mock

import pytest

from chronal_api.lib.auth import exceptions as auth_service_exceptions
from chronal_api.lib.auth import models as auth_models
from chronal_api.lib.auth import service as auth_service_


@pytest.fixture
def auth_service() -> auth_service_.AuthService:
    return auth_service_.AuthService(mock.AsyncMock())


def test_auth_service_init():
    repository = mock.Mock()
    service = auth_service_.AuthService(repository)

    assert service.repository == repository


async def test_create_token(auth_service: auth_service_.AuthService):
    user = mock.Mock()

    await auth_service.create_token(user)
    auth_service.repository.create_token.assert_called_once_with(user)


async def test_delete_token(auth_service: auth_service_.AuthService):
    token = "token123"
    auth_service.repository.exists.return_value = True

    await auth_service.delete_token(token)
    auth_service.repository.delete.assert_called_once_with(id=token)


async def test_delete_token_raises_invalid_token(auth_service: auth_service_.AuthService):
    token = "token123"
    auth_service.repository.exists.return_value = False

    with pytest.raises(auth_service_exceptions.InvalidAccessToken):
        await auth_service.delete_token(token)

    auth_service.repository.delete.assert_not_called()


@mock.patch("chronal_api.lib.auth.security.verify_password")
async def test_authenticate(
    mock_verify_password: mock.MagicMock, auth_service: auth_service_.AuthService
):
    user = mock.Mock()
    user.hashed_password = "123123123123123"
    mock_verify_password.return_value = True

    await auth_service.authenticate(user, "password")
    mock_verify_password.assert_called_once_with("password", user.hashed_password)


@mock.patch("chronal_api.lib.auth.security.verify_password")
async def test_authenticate_raises_wrong_password(
    mock_verify_password: mock.MagicMock, auth_service: auth_service_.AuthService
):
    user = mock.Mock()
    user.hashed_password = "123123123123123"
    mock_verify_password.return_value = False

    with pytest.raises(auth_service_exceptions.WrongPassword):
        await auth_service.authenticate(user, "password")


async def test_validate_access_token(auth_service: auth_service_.AuthService):
    expiration_date = datetime(2077, 8, 20, tzinfo=timezone.utc)
    access_token = auth_models.AccessToken(access_token="token", expiration_date=expiration_date)
    auth_service.repository.get_one_or_none.return_value = access_token

    token = await auth_service.validate_access_token("token")
    assert token


async def test_validate_access_token_raises_invalidate_access_token(
    auth_service: auth_service_.AuthService,
):
    auth_service.repository.get_one_or_none.return_value = None
    with pytest.raises(auth_service_exceptions.InvalidAccessToken):
        await auth_service.validate_access_token("token")


async def test_validate_access_token_raises_expired_access_token(
    auth_service: auth_service_.AuthService,
):
    expiration_date = datetime(1999, 8, 20, tzinfo=timezone.utc)
    access_token = auth_models.AccessToken(access_token="token", expiration_date=expiration_date)
    auth_service.repository.get_one_or_none.return_value = access_token

    with pytest.raises(auth_service_exceptions.ExpiredAccessToken):
        await auth_service.validate_access_token("token")
