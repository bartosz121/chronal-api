from enum import Enum
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from chronal_api import __version__


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

    DB: str = "postgres"
    USER: str = "chronal"
    PASSWORD: str = "pa$$w0rd123!@#"
    HOST: str = "127.0.0.1"
    PORT: int = 5432
    NAME: str = "chronaldb"
    DRIVER: str = "asyncpg"

    @property
    def url(self) -> str:
        if self.DB == "sqlite":
            return "{}+{}://{}".format(self.DB, self.DRIVER, self.HOST)
        else:
            return "{}+{}://{}:{}@{}:{}/{}".format(
                self.DB,
                self.DRIVER,
                self.USER,
                self.PASSWORD,
                self.HOST,
                self.PORT,
                self.NAME,
            )


class ChronalSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CHRONAL_")

    TITLE: str = "Chronal API"
    VERSION: str = __version__
    ENVIRONMENT: Environment = Environment.LOCAL
    ROOT_PATH: str = "/"
    DEBUG: bool = True


@lru_cache(maxsize=1)
def get_app_settings() -> ChronalSettings:
    return ChronalSettings()
