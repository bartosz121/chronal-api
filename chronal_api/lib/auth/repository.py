from typing import TYPE_CHECKING

from chronal_api.lib.repository.sqlalchemy import SQLAlchemyRepository

from . import models

if TYPE_CHECKING:
    from chronal_api.users.models import User


class AccessTokenRepository(SQLAlchemyRepository[models.AccessToken, str]):
    model = models.AccessToken
    model_id_attr_name = "access_token"

    async def create_token(self, user: "User") -> models.AccessToken:
        token = await self.create(models.AccessToken(user=user))
        return token
