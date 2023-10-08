from unittest import mock

import pytest

from chronal_api.users import models as users_models
from chronal_api.users import repository as users_repository


@pytest.fixture
def user_repository_unit() -> users_repository.UserRepository:
    return users_repository.UserRepository(mock.AsyncMock())


@mock.patch.object(users_repository.UserRepository, "_expunge")
async def test_get_by_email(
    _: mock.AsyncMock,
    user_repository_unit: users_repository.UserRepository,
):
    execute_return = mock.Mock()
    user_repository_unit.session.execute.return_value = execute_return
    user = mock.MagicMock(spec=users_models.User)
    execute_return.scalar_one_or_none.return_value = user

    u = await user_repository_unit.get_by_email("email")
    assert u


@mock.patch.object(users_repository.UserRepository, "_expunge")
async def test_get_by_email_returns_none_if_not_found(
    _: mock.AsyncMock,
    user_repository_unit: users_repository.UserRepository,
):
    execute_return = mock.Mock()
    user_repository_unit.session.execute.return_value = execute_return
    execute_return.scalar_one_or_none.return_value = None

    u = await user_repository_unit.get_by_email("email")
    assert u is None


@mock.patch.object(users_repository.UserRepository, "exists")
async def test_email_exists(
    mock_exists: mock.AsyncMock, user_repository_unit: users_repository.UserRepository
):
    await user_repository_unit.email_exists("email")
    mock_exists.assert_called_once_with(email="email")


@mock.patch("chronal_api.users.models.User")
@mock.patch.object(users_repository.UserRepository, "create")
async def test_create_user(
    mock_create: mock.AsyncMock,
    mock_user: mock.MagicMock,
    user_repository_unit: users_repository.UserRepository,
):
    user = mock.Mock()
    mock_user.return_value = user

    r = await user_repository_unit.create_user("email", "hashed_password")

    mock_user.assert_called_once_with(email="email", hashed_password="hashed_password")
    mock_create.assert_called_once_with(user)

    assert r
