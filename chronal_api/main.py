import uvicorn
import logging
from pkg_resources import resource_filename

from alembic.command import upgrade
from alembic.config import Config
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from chronal_api.auth import fastapi_users, auth_backend
from chronal_api.core import debug
from chronal_api.core.config import get_config
from chronal_api.schemas import UserCreate, UserRead, UserUpdate
from chronal_api.utils import create_router_prefix

config = get_config()

app = FastAPI(
    title=config.TITLE,
    version=config.VERSION,
    root_path=config.ROOT_PATH,
    docs_url=None if config.DISABLE_DOCS else "/docs",
    redoc_url=None if config.DISABLE_DOCS else "/redoc",
)

if config.IS_DEV:
    app.add_middleware(debug.TimerMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(debug.RequestLoggingMiddleware)


@app.on_event("startup")
def run_migrations():
    config = Config(resource_filename("chronal_api", "alembic.ini"))
    upgrade(config, "head")


# FastAPI users --------------------
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=create_router_prefix("/auth/jwt"),
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=create_router_prefix("/auth"),
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix=create_router_prefix("/auth"),
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix=create_router_prefix("/auth"),
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix=create_router_prefix("/users"),
    tags=["users"],
)
# ----------------------------------


@app.get("/")
def home():
    return {"msg": config.TITLE}


@app.get("/config")
def show_config():
    return config


def run():
    uvicorn.run(
        "chronal_api.main:app",
        log_config=debug.LOGGING_CONFIG,
        reload=config.UVICORN_RELOAD,
        workers=config.UVICORN_WORKERS,
        host=config.UVICORN_HOST,
        port=config.UVICORN_PORT,
    )


if __name__ == "__main__":
    run()
