import random
from typing import Any

import factory
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from faker import Faker

from chronal_api.calendars import models as calendars_models
from chronal_api.lib.auth import models as auth_models
from chronal_api.lib.auth import security
from chronal_api.users import models as users_models

from .database import Session

fake = Faker()


class BaseFactory(AsyncSQLAlchemyFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"


class UserFactory(BaseFactory):
    _DEFAULT_PASSWORD = "passw0rd123!@#"
    custom_password = None

    class Meta:
        model = users_models.User
        exclude = ("custom_password",)

    email = factory.Faker("email")
    hashed_password = factory.LazyAttribute(
        lambda obj: security.get_password_hash(
            obj.custom_password
            if obj.custom_password is not None
            else UserFactory._DEFAULT_PASSWORD
        )
    )

    @classmethod
    def _create(cls, model_class, *args: Any, **kwargs: Any):
        if factory_custom_password := kwargs.get("custom_password"):
            kwargs["hashed_password"] = security.get_password_hash(factory_custom_password)
        return super()._create(model_class, *args, **kwargs)


class AccessTokenFactory(BaseFactory):
    class Meta:
        model = auth_models.AccessToken

    user = factory.SubFactory(UserFactory)


class CalendarFactory(BaseFactory):
    class Meta:
        model = calendars_models.Calendar

    title = factory.LazyAttribute(lambda _: fake.text(random.randint(16, 250)))
    description = factory.LazyAttribute(
        lambda _: fake.text(random.randint(5, 300))
        if random.choice(
            (
                True,
                False,
            )
        )
        else None
    )
    owner = factory.SubFactory(UserFactory)
