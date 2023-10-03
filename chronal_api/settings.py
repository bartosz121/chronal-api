from enum import Enum
from functools import lru_cache
from typing import TYPE_CHECKING, Any

from pydantic_settings import BaseSettings, SettingsConfigDict

from chronal_api import __version__

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


class Environment(str, Enum):
    LOCAL = "LOCAL"
    TESTING = "TESTING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_local(self) -> bool:
        return self == Environment.LOCAL

    @property
    def is_testing(self) -> bool:
        return self == Environment.TESTING

    @property
    def is_production(self) -> bool:
        return self == Environment.PRODUCTION


class UvicornSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="UVICORN_", case_sensitive=False)

    host: str = "127.0.0.1"
    port: int = 8080
    workers: int = 1
    reload: bool = True


class CORSSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CORS_", case_sensitive=False)

    allow_origins: list[str] = ["*"]
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]
    allow_credentials: bool = True


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_")

    DB: str = "sqlite"
    USER: str = "chronal"
    PASSWORD: str = "pa$$w0rd123!@#"
    HOST: str = "//tmp/chronal.db"
    PORT: int = 5432
    NAME: str = "chronaldb"
    DRIVER: str = ""
    ASYNC_DRIVER: str = "aiosqlite"
    ECHO: bool = False

    def get_url(self, *, async_=True, **kwargs: Any) -> "URL":
        from sqlalchemy import engine

        driver = self.ASYNC_DRIVER if async_ else self.DRIVER
        drivername = self.DB if not driver else f"{self.DB}+{driver}"

        if self.DB == "sqlite":
            url = url = engine.URL.create(
                drivername,
                host=self.HOST,
                **kwargs,
            )
        else:
            url = engine.URL.create(
                drivername,
                self.USER,
                self.PASSWORD,
                self.HOST,
                self.PORT,
                self.NAME,
                **kwargs,
            )

        return url


class ChronalSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CHRONAL_")

    TITLE: str = "Chronal API"
    VERSION: str = __version__
    ENVIRONMENT: Environment = Environment.LOCAL
    ROOT_PATH: str = "/"
    DEBUG: bool = True
    TOKEN_DURATION: int = 604800  # 7 days


@lru_cache(maxsize=1)
def get_app_settings() -> ChronalSettings:
    return ChronalSettings()
