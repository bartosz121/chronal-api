from uuid import UUID

from chronal_api.lib.auth import security as auth_security
from chronal_api.lib.service import Service

from . import exceptions, models, repository, schemas


class UserService(Service[models.User, UUID]):
    def __init__(self, repository: repository.UserRepository) -> None:
        """UserService"""
        self.repository = repository

    async def create_user(self, data: schemas.UserCreate) -> models.User:
        hashed_password = auth_security.get_password_hash(data.password)

        email_exists = await self.repository.email_exists(data.email)
        if email_exists:
            raise exceptions.EmailAlreadyExists()

        return await self.repository.create_user(data.email, hashed_password)

    async def get_by_email(self, email: str) -> models.User:
        user = await self.repository.get_by_email(email)
        if user is None:
            raise exceptions.UserNotFound()
        return user
