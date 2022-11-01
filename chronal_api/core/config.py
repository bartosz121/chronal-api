from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn

from chronal_api import __version__


class Config(BaseSettings):
    TITLE: str = f"Chronal API {__version__}"
    VERSION: str = __version__
    ROOT_PATH: str = ""
    API_PREFIX: str = "/api/v1"
    DISABLE_DOCS: bool = False
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


def get_config():
    return Config()
