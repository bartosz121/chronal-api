import uuid
import logging
from typing import Optional

from fastapi import Request, Depends
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from chronal_api.core.config import get_config
from chronal_api.db import chronal_psql
from chronal_api.models import User

config = get_config()


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = config.SECRET
    verification_token_secret = config.SECRET

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        logging.debug("User %s had been registered", user.id)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        logging.debug(
            "User %s has forgot their password. Reset token: %s", user.id, token
        )

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        logging.debug(
            "Verification requested for user %s. Verification token: %s", user.id, token
        )


async def get_user_db(session: AsyncSession = Depends(chronal_psql.get_psql_db)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
