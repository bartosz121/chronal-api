from unittest import mock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from chronal_api.lib.repository.exceptions import RepositoryException
from chronal_api.lib.repository.sqlalchemy import SQLAlchemyRepository

AnyMock = mock.MagicMock | mock.AsyncMock


@pytest.fixture
def sqlalchemy_repository() -> SQLAlchemyRepository:
    class Repository_(SQLAlchemyRepository[mock.MagicMock, int]):
        model = mock.MagicMock

    return Repository_(
        session=mock.AsyncMock(spec=AsyncSession, bind=mock.MagicMock()),
        statement=mock.MagicMock(),
    )


async def test_sqlalchemy_repository__attach_to_session_raises_repository_exception_on_wrong_strategy(  # noqa: E501
    sqlalchemy_repository: SQLAlchemyRepository,
):
    with pytest.raises(RepositoryException, match="Strategy must be 'add' or 'merge', found:"):
        await sqlalchemy_repository._attach_to_session(
            mock.MagicMock(), "wrong strategy"  # pyright: ignore
        )


async def test_sqlalchemy__flush_or_commit_commit_if_auto_commit(
    sqlalchemy_repository: SQLAlchemyRepository,
):
    await sqlalchemy_repository._flush_or_commit(auto_commit=True)
    sqlalchemy_repository.session.commit.assert_called_once()


async def test_sqlalchemy__refresh_refresh_not_called_if_auto_refresh_is_false(
    sqlalchemy_repository: SQLAlchemyRepository,
):
    await sqlalchemy_repository._refresh(mock.MagicMock(), auto_refresh=False)
    sqlalchemy_repository.session.refresh.assert_not_called()


async def test_sqlalchemy__expunge_expunge_called_if_auto_expunge_is_true(
    sqlalchemy_repository: SQLAlchemyRepository,
):
    await sqlalchemy_repository._expunge(mock.MagicMock(), auto_expunge=True)
    sqlalchemy_repository.session.expunge.assert_called_once()
