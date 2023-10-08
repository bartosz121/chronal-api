from fastapi import HTTPException, Request, Response, status
from fastapi.security import HTTPBearer

from chronal_api.lib import schemas as api_schemas
from chronal_api.lib.auth import dependencies as auth_dependencies
from chronal_api.lib.auth import exceptions as auth_exceptions
from chronal_api.lib.router import APIRouter

from . import dependencies, exceptions, schemas

router = APIRouter(
    tags=["users"],
    api_routes_responses={
        "users:register": {
            status.HTTP_201_CREATED: {
                "description": "User successfully registered",
                "model": schemas.UserRead,
            },
            status.HTTP_409_CONFLICT: {
                "description": "Email address already in use",
                "model": api_schemas.Message,
                "content": {
                    "application/json": {
                        "example": {"msg": exceptions.HTTPError.EMAIL_ALREADY_IN_USE}
                    }
                },
            },
        },
        "users:token": {
            status.HTTP_201_CREATED: {
                "description": "Token successfully created",
                "model": schemas.AccessToken,
            },
            status.HTTP_400_BAD_REQUEST: {
                "description": "Bad request",
                "model": api_schemas.Message,
                "content": {
                    "application/json": {
                        "examples": {
                            "Wrong password": {
                                "value": {"msg": exceptions.HTTPError.WRONG_PASSWORD},
                            }
                        }
                    }
                },
            },
            status.HTTP_404_NOT_FOUND: {
                "description": "User with given email does not exist",
                "model": api_schemas.Message,
                "content": {
                    "application/json": {"example": {"msg": exceptions.HTTPError.EMAIL_NOT_FOUND}}
                },
            },
        },
        "users:logout": {
            status.HTTP_204_NO_CONTENT: {"description": "User successfully logged out"}
        },
    },
)


@router.post(
    "/register",
    name="users:register",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserRead,
)
async def register(
    user_create: schemas.UserCreate,
    user_service: dependencies.UserService,
):
    try:
        user = await user_service.create_user(user_create)
    except exceptions.EmailAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"msg": exceptions.HTTPError.EMAIL_ALREADY_IN_USE},
        )
    else:
        return user


@router.post(
    "/token",
    name="users:token",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.AccessToken,
)
async def create_token(
    data: schemas.CreateToken,
    user_service: dependencies.UserService,
    auth_service: auth_dependencies.AuthService,
):
    try:
        user = await user_service.get_by_email(data.email)
        await auth_service.authenticate(user, data.password)
    except exceptions.UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": exceptions.HTTPError.EMAIL_NOT_FOUND},
        )
    except auth_exceptions.WrongPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"msg": exceptions.HTTPError.WRONG_PASSWORD},
        )
    else:
        token = await auth_service.create_token(user)
        return {"access_token": token.access_token, "token_type": "bearer"}


@router.get(
    "/logout",
    name="users:logout",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def logout(
    request: Request,
    user: auth_dependencies.OptionalCurrentUser,
    auth_service: auth_dependencies.AuthService,
):
    if user:
        bearer = HTTPBearer(auto_error=False)
        security = await bearer(request)
        if security:
            await auth_service.delete_token(security.credentials)
