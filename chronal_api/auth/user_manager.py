import logging
import uuid
from typing import Optional

from fastapi import Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from chronal_api.core.config import get_config

from .models import User

config = get_config()


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = config.SECRET
    verification_token_secret = config.SECRET

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        logging.debug("User %s has registered", user.id)

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
