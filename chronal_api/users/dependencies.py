from typing import Annotated

from fastapi import Depends

from chronal_api.lib.database import dependencies as db_dependencies

from . import repository, service


async def user_service(session: db_dependencies.DbSession):
    return service.UserService(repository.UserRepository(session))


# Annotated

UserService = Annotated[service.UserService, Depends(user_service)]
