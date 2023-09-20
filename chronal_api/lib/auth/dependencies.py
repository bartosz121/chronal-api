from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer as HTTPBearer_
from fastapi.security import utils as fastapi_security_utils
from fastapi.security.http import HTTPAuthorizationCredentials
from starlette.requests import Request

from chronal_api.lib.database import dependencies as db_dependencies
from chronal_api.users.models import User

from . import exceptions, repository, service


class HTTPBearer(HTTPBearer_):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        authorization = request.headers.get("Authorization")
        scheme, credentials = fastapi_security_utils.get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            return None
        if scheme.lower() != "bearer":
            return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


authorization_bearer = HTTPBearer()


async def auth_service(
    session: db_dependencies.DbSession,
) -> service.AuthService:
    return service.AuthService(repository.AccessTokenRepository(session))


async def get_current_user(
    security: HTTPAuthorizationCredentials | None = Depends(authorization_bearer),
    auth_service: service.AuthService = Depends(auth_service),
) -> User:
    if security is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "Unauthorized"}
        )

    try:
        access_token = await auth_service.validate_access_token(security.credentials)
    except (exceptions.InvalidAccessToken, exceptions.ExpiredAccessToken) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "Unauthorized"}
        ) from exc
    else:
        return access_token.user


async def get_optional_current_user(
    security: HTTPAuthorizationCredentials | None = Depends(authorization_bearer),
    auth_service: service.AuthService = Depends(auth_service),
) -> User | None:
    if security is None:
        return None

    try:
        access_token = await auth_service.validate_access_token(security.credentials)
    except (exceptions.InvalidAccessToken, exceptions.ExpiredAccessToken):
        return None
    else:
        return access_token.user


# Annotated

AuthService = Annotated[service.AuthService, Depends(auth_service)]
CurrentUser = Annotated[User, Depends(get_current_user)]
OptionalCurrentUser = Annotated[User | None, Depends(get_optional_current_user)]
