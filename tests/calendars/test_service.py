import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from chronal_api.calendars import exceptions as calendars_exceptions
from chronal_api.calendars import models as calendars_models
from chronal_api.calendars import schemas as calendars_schemas
from chronal_api.calendars import service as calendars_service
from tests import factories


async def test_user_is_calendar_owner(
    calendar_service: calendars_service.CalendarService,
    calendar_factory: factories.CalendarFactory,
    user_factory: factories.UserFactory,
):
    user = await user_factory.create()
    calendar_1 = await calendar_factory.create(owner=user)
    assert await calendar_service.is_calendar_owner(user.id, calendar_1.id) is True

    calendar_2 = await calendar_factory.create()
    assert await calendar_service.is_calendar_owner(user.id, calendar_2.id) is False


async def test_create_calendar(
    session: AsyncSession,
    calendar_service: calendars_service.CalendarService,
    calendar_factory: factories.CalendarFactory,
    user_factory: factories.UserFactory,
):
    user = await user_factory.create()
    cal = calendar_factory.build(owner=user)

    data = calendars_schemas.CalendarCreate(title=cal.title, description=cal.description)
    calendar = await calendar_service.create_calendar(data, user.id)

    exists = (
        await session.execute(
            select(calendars_models.Calendar).where(calendars_models.Calendar.id == calendar.id)
        )
    ).scalar_one_or_none()
    assert exists is not None


async def test_create_calendar_raises_title_not_unique(
    calendar_service: calendars_service.CalendarService,
    calendar_factory: factories.CalendarFactory,
    user_factory: factories.UserFactory,
):
    user = await user_factory.create()
    cal = await calendar_factory.create(owner=user)

    data = calendars_schemas.CalendarCreate(title=cal.title, description=cal.description)
    with pytest.raises(calendars_exceptions.TitleNotUnique):
        await calendar_service.create_calendar(data, user.id)


async def test_update(
    session: AsyncSession,
    calendar_service: calendars_service.CalendarService,
    calendar_factory: factories.CalendarFactory,
):
    TITLE = "updated title"

    cal = await calendar_factory.create()
    data = calendars_schemas.CalendarPatch(title=TITLE)
    calendar = await calendar_service.update_calendar(cal, data)

    assert calendar.title == TITLE

    cal_db = (
        await session.execute(
            select(calendars_models.Calendar).where(calendars_models.Calendar.id == calendar.id)
        )
    ).scalar_one_or_none()

    assert cal_db is not None
    assert cal_db.title == TITLE


async def test_update_raises_title_not_unique(
    calendar_service: calendars_service.CalendarService,
    calendar_factory: factories.CalendarFactory,
    user_factory: factories.UserFactory,
):
    user = await user_factory.create()
    cal_1 = await calendar_factory.create(owner=user)
    cal_2 = await calendar_factory.create(owner=user)
    data = calendars_schemas.CalendarPatch(title=cal_1.title)

    with pytest.raises(calendars_exceptions.TitleNotUnique):
        await calendar_service.update_calendar(cal_2, data)


async def test_delete(
    session: AsyncSession,
    calendar_service: calendars_service.CalendarService,
    calendar_factory: factories.CalendarFactory,
):
    calendar = await calendar_factory.create()

    await calendar_service.delete(calendar.id)

    exists = (
        await session.execute(
            select(calendars_models.Calendar).where(calendars_models.Calendar.id == calendar.id)
        )
    ).scalar_one_or_none()
    assert exists is None
