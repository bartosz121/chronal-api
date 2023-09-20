import uuid
from datetime import datetime, timezone

from chronal_api.lib.service import Service
from chronal_api.users.models import User

from . import exceptions, models, repository, security


class AuthService(Service[models.AccessToken, uuid.UUID]):
    def __init__(self, repository: repository.AccessTokenRepository) -> None:
        """AuthService"""
        self.repository = repository

    async def create_token(self, user: User) -> models.AccessToken:
        return await self.repository.create_token(user)

    async def delete_token(self, access_token: str) -> None:
        token_exists = await self.repository.exists(access_token=access_token)
        if token_exists:
            await self.repository.delete(id=access_token)
        else:
            raise exceptions.InvalidAccessToken()

    async def authenticate(self, user: User, plain_password: str) -> User:
        if not security.verify_password(plain_password, user.hashed_password):
            raise exceptions.WrongPassword()
        return user

    async def validate_access_token(self, access_token: str) -> models.AccessToken:
        db_access_token = await self.repository.get_one_or_none(access_token)

        if db_access_token is None:
            raise exceptions.InvalidAccessToken()

        if db_access_token.expiration_date <= datetime.now(tz=timezone.utc):
            # TODO: schedule task to remove expired token
            raise exceptions.ExpiredAccessToken()

        return db_access_token


# TODO: cors/csrf, tests
