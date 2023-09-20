import secrets
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext

from chronal_api.settings import get_app_settings

settings = get_app_settings()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_token() -> str:
    return secrets.token_urlsafe(32)


def generate_token_expiration_date(duration_seconds: int = settings.TOKEN_DURATION) -> datetime:
    return datetime.now(tz=timezone.utc) + timedelta(seconds=duration_seconds)
