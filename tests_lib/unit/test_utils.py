import pytest
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from chronal_api.lib.repository import exceptions as repository_exceptions
from chronal_api.lib.repository.utils import sql_error_handler


async def test_sql_error_handler_raises_conflict_error_on_integrity_error():
    with pytest.raises(repository_exceptions.ConflictError) as exc:
        async with sql_error_handler():
            raise IntegrityError("", None, Exception())

    assert isinstance(exc.value.__cause__, IntegrityError)


async def test_sql_error_handler_raises_repository_exception_on_sqlalchemy_error():
    with pytest.raises(repository_exceptions.RepositoryException) as exc:
        async with sql_error_handler():
            raise SQLAlchemyError()

    assert isinstance(exc.value.__cause__, SQLAlchemyError)


async def test_sql_error_handler_raises_repository_exception_on_integrity_error():
    with pytest.raises(repository_exceptions.RepositoryException) as exc:
        async with sql_error_handler():
            raise AttributeError()

    assert isinstance(exc.value.__cause__, AttributeError)
