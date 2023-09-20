from fastapi import HTTPException, Request, Response, status
from fastapi.security import HTTPBearer

from chronal_api.lib import schemas as api_schemas
from chronal_api.lib.auth import dependencies as auth_dependencies
from chronal_api.lib.auth import exceptions as auth_exceptions
from chronal_api.lib.router import APIRouter

from . import dependencies, schemas, service

router = APIRouter(
    tags=["users"],
    api_routes_responses={
        "/register": {
            201: {
                "description": "User successfully registered",
                "model": schemas.UserRead,
            },
            409: {
                "description": "Email address already in use",
                "model": api_schemas.Message,
                "content": {"application/json": {"example": {"msg": "Email already in use"}}},
            },
        },
        "/token": {
            201: {"description": "Token successfully created", "model": schemas.AccessToken},
            404: {
                "description": "User with given email does not exist",
                "model": api_schemas.Message,
                "content": {
                    "application/json": {"example": {"msg": "User with this email does not exist"}}
                },
            },
            400: {
                "description": "Bad request",
                "model": api_schemas.Message,
                "content": {
                    "application/json": {
                        "examples": {
                            "Wrong password": {
                                "value": {"msg": "Wrong password"},
                            }
                        }
                    }
                },
            },
        },
        "/logout": {204: {"description": "User successfully logged out"}},
    },
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRead)
async def register(
    user_create: schemas.UserCreate,
    user_service: dependencies.UserService,
):
    try:
        user = await user_service.create_user(user_create)
    except service.EmailAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail={"msg": "Email already in use"}
        )
    else:
        return user


@router.post("/token", status_code=status.HTTP_201_CREATED, response_model=schemas.AccessToken)
async def create_token(
    data: schemas.CreateToken,
    user_service: dependencies.UserService,
    auth_service: auth_dependencies.AuthService,
):
    try:
        user = await user_service.get_by_email(data.email)
    except service.UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "User with this email does not exist"},
        )

    try:
        await auth_service.authenticate(user, data.password)
    except auth_exceptions.WrongPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"msg": "Wrong password"}
        )

    token = await auth_service.create_token(user)
    return {"access_token": token.access_token, "token_type": "bearer"}


@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
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
