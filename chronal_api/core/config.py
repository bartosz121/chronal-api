from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn

from chronal_api import __version__


class Config(BaseSettings):
    TITLE: str = f"Chronal API {__version__}"
    VERSION: str = __version__
    ROOT_PATH: str = ""
    API_PREFIX: str = "/api/v1"
    DOCS_URL: str | None = "/docs"
    REDOC_URL: str | None = "/redoc"
    IS_DEV: bool = True
    # CORS
    ALLOWED_ORIGINS: str

    # uvicorn
    UVICORN_RELOAD: bool
    UVICORN_WORKERS: int
    UVICORN_HOST: str
    UVICORN_PORT: int

    # Databases
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    # SQLALCHEMY_DB_URI: PostgresDsn

    # Email
    # TODO

    class Config:
        case_sensitive = True


def get_config(local=False):
    if local:
        return Config(
            ALLOWED_ORIGINS="[*]",
            UVICORN_RELOAD=True,
            UVICORN_WORKERS=1,
            UVICORN_HOST="0.0.0.0",
            UVICORN_PORT=8081,
            POSTGRES_SERVER="x",
            POSTGRES_USER="x",
            POSTGRES_PASSWORD="x",
            POSTGRES_DB="x",
        )
    return Config()
