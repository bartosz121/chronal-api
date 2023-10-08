from chronal_api.calendars import repository as calendars_repository
from tests import factories


async def test_user_is_calendar_owner(
    calendar_repository: calendars_repository.CalendarRepository,
    calendar_factory: factories.CalendarFactory,
    user_factory: factories.UserFactory,
):
    user = await user_factory.create()
    calendar_1 = await calendar_factory.create(owner=user)

    calendar_1_is_user_owner = await calendar_repository.user_is_calendar_owner(
        user.id, calendar_1.id
    )
    assert calendar_1_is_user_owner is True

    calendar_2 = await calendar_factory.create()
    calendar_2_is_user_owner = await calendar_repository.user_is_calendar_owner(
        user.id, calendar_2.id
    )
    assert calendar_2_is_user_owner is False


async def test_calendar_title_exists_for_user(
    calendar_repository: calendars_repository.CalendarRepository,
    calendar_factory: factories.CalendarFactory,
    user_factory: factories.UserFactory,
):
    TITLE = "title_1"
    user = await user_factory.create()
    await calendar_factory.create(title=TITLE, owner=user)

    assert await calendar_repository.title_exists_for_user(user.id, TITLE) is True
    assert await calendar_repository.title_exists_for_user(user.id, "title_2") is False
