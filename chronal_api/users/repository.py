from uuid import UUID

from chronal_api.lib.repository.sqlalchemy import SQLAlchemyRepository
from chronal_api.lib.repository.utils import sql_error_handler

from . import models


class UserRepository(SQLAlchemyRepository[models.User, UUID]):
    model = models.User

    async def get_by_email(
        self, email: str, auto_expunge: bool | None = None
    ) -> models.User | None:
        statement = self.statement.where(models.User.email == email)

        async with sql_error_handler():
            instance = (await self.session.execute(statement)).scalar_one_or_none()
            if instance is None:
                return None

            await self._expunge(instance, auto_expunge=auto_expunge)
            return instance

    async def email_exists(self, email: str) -> bool:
        return await self.exists(email=email)

    async def create_user(self, email: str, hashed_password: str) -> models.User:
        user = models.User(email=email, hashed_password=hashed_password)
        return await self.create(user)
