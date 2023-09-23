from unittest import mock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from chronal_api.lib.auth import repository as auth_repository


@pytest.fixture
def access_token_repo() -> auth_repository.AccessTokenRepository:
    return auth_repository.AccessTokenRepository(
        session=mock.AsyncMock(spec=AsyncSession, bind=mock.MagicMock())
    )


@mock.patch("chronal_api.lib.auth.models.AccessToken")
@mock.patch.object(auth_repository.AccessTokenRepository, "create")
async def test_create_token(
    mock_create: mock.AsyncMock,
    mock_access_token: mock.MagicMock,
    access_token_repo: auth_repository.AccessTokenRepository,
):
    user = mock.Mock()
    await access_token_repo.create_token(user)
    mock_access_token.assert_called_once_with(user=user)
    mock_create.assert_called_once()
