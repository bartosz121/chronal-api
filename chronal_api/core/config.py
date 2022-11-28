from functools import lru_cache
from typing import Any

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, SecretStr

from chronal_api import __version__


class Config(BaseSettings):
    TITLE: str = f"Chronal API {__version__}"
    VERSION: str = __version__
    ROOT_PATH: str = ""
    API_PREFIX: str = "/api/v1"
    IS_DEV: bool = True
    SECRET: str | SecretStr
    # CORS
    ALLOWED_ORIGINS: str

    # uvicorn
    UVICORN_RELOAD: bool
    UVICORN_WORKERS: int
    UVICORN_HOST: str
    UVICORN_PORT: int

    # Databases
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    # SQLALCHEMY_DB_URI: PostgresDsn

    # Email
    # TODO

    # Pydantic
    PDNT_BLACKLIST_NAMES: tuple[str, ...] = (
        "admin",
        "owner",
    )

    @property
    def postgres_uri(self) -> str:
        return self._postgres_uri("asyncpg")

    @property
    def postgres_uri_psycopg2(self) -> str:
        return self._postgres_uri("psycopg2")

    def _postgres_uri(self, driver: str) -> str:
        return self._build_db_uri(
            "postgresql",
            driver,
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_SERVER,
            self.POSTGRES_PORT,
            self.POSTGRES_DB,
        )

    def _build_db_uri(
        self,
        db: str,
        driver: str,
        user: str,
        password: str,
        server: str,
        port: str,
        db_name: str,
    ) -> str:
        return "{}+{}://{}:{}@{}:{}/{}".format(
            db, driver, user, password, server, port, db_name
        )

    class Config:
        case_sensitive = True


class TestConfig(Config):
    TEST_POSTGRES_SERVER: str
    TEST_POSTGRES_PORT: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_DB: str

    @property
    def test_postgres_uri(self) -> str:
        return self._build_db_uri(
            "postgresql",
            "asyncpg",
            self.TEST_POSTGRES_USER,
            self.TEST_POSTGRES_PASSWORD,
            self.TEST_POSTGRES_SERVER,
            self.TEST_POSTGRES_PORT,
            self.TEST_POSTGRES_DB,
        )


@lru_cache(maxsize=1)
def get_config() -> Config:
    return Config()  # type: ignore https://github.com/pydantic/pydantic/issues/3753
