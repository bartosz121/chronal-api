from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from chronal_api.log import get_logger

from .exceptions import Conflict, RepositoryException

logger = get_logger()


@asynccontextmanager
async def sql_error_handler() -> AsyncIterator[None]:
    try:
        yield
    except IntegrityError as e:
        logger.error(str(e))
        raise Conflict from e
    except SQLAlchemyError as e:
        logger.error(str(e))
        raise RepositoryException("An exception occurred while executing a SQL statement.") from e
    except AttributeError as e:
        logger.error(str(e))
        raise RepositoryException from e
