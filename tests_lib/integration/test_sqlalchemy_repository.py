import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from chronal_api.lib.repository import exceptions as repo_exceptions
from chronal_api.lib.repository.sqlalchemy import SQLAlchemyRepository

from ..conftest import DUMMY_COUNT
from ..models import TodoItem


class TodoItemRepository(SQLAlchemyRepository[TodoItem, int]):
    model = TodoItem


@pytest.fixture(scope="function")
async def repo(session) -> SQLAlchemyRepository[TodoItem, int]:
    return TodoItemRepository(session)


async def test_count(insert_dummy, repo: TodoItemRepository):
    repo_count = await repo.count()
    assert repo_count == DUMMY_COUNT


async def test_count_kwargs(session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(
        title="Test count kwargs",
        description="test count kwargs desc",
        is_completed=False,
    )
    session.add(item)
    await session.commit()

    repo_count = await repo.count(
        title=item.title,
        description=item.description,
        is_completed=item.is_completed,
    )
    assert repo_count == 1


async def test_create(session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(
        title="Test create",
        description="test create desc",
        is_completed=False,
    )
    created = await repo.create(item)
    assert created == item
    assert created.id

    item_from_db = (
        await session.execute(select(TodoItem).where(TodoItem.title == "Test create"))
    ).scalar_one_or_none()
    assert item_from_db is not None
    assert item_from_db.id == created.id


async def test_create_many(session: AsyncSession, repo: TodoItemRepository):
    items = [
        TodoItem(
            title=f"Test create_many {i}",
            description=f"test create_many {i}",
            is_completed=False,
        )
        for i in range(10)
    ]

    created = await repo.create_many(items)
    assert created == items
    assert all((item.id for item in created))

    items_from_db = (
        (await session.execute(select(TodoItem).where(TodoItem.title.like("Test create_many%"))))
        .scalars()
        .all()
    )

    assert len(items_from_db) == len(items)
    assert all((item.id in [i.id for i in items_from_db] for item in items))


async def test_delete(session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(
        title="Test delete",
        description="test delete desc",
        is_completed=False,
    )
    session.add(item)
    await session.commit()

    deleted = await repo.delete(item.id)
    assert deleted == item

    should_be_none = (
        await session.execute(select(TodoItem).where(TodoItem.id == item.id))
    ).scalar_one_or_none()
    assert should_be_none is None


async def test_delete_raises_not_found(session: AsyncSession, repo: TodoItemRepository):
    with pytest.raises(repo_exceptions.NotFound):
        await repo.delete(454544545)


# Check your sqlite version if this fails, delete_many uses
# `RETURNING` which is supported in 3.35.0+
async def test_delete_many(session: AsyncSession, repo: TodoItemRepository):
    items = [
        TodoItem(
            title=f"Test delete_many {i}",
            description=f"test delete_many {i}",
            is_completed=False,
        )
        for i in range(10)
    ]

    session.add_all(items)
    await session.commit()

    deleted = await repo.delete_many([item.id for item in items])
    assert len(deleted) == len(items)
    assert all((item.title in [i.title for i in deleted] for item in items))

    items_from_db = (
        (await session.execute(select(TodoItem).where(TodoItem.title.like("Test delete_many%"))))
        .scalars()
        .all()
    )
    assert items_from_db == []


async def test_exists(session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(
        title="Test exists",
        description="test exists desc",
        is_completed=False,
    )
    session.add(item)
    await session.commit()

    assert (await repo.exists(id=item.id)) is True
    assert (await repo.exists(title=item.title)) is True
    assert (await repo.exists(description=item.description)) is True


async def test_exists_false(repo: TodoItemRepository):
    assert (await repo.exists(id=999999)) is False
    assert (await repo.exists(title="Test exists")) is False
    assert (await repo.exists(description="test exists desc")) is False


async def test_get(session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(
        title="Test get",
        description="test get desc",
        is_completed=False,
    )
    session.add(item)
    await session.commit()

    item_from_db = await repo.get(item.id)
    assert vars(item) == vars(item_from_db)


async def test_get_raises_not_found(repo: TodoItemRepository):
    with pytest.raises(repo_exceptions.NotFound):
        await repo.get(999999)


async def test_get_one_raises_not_found(
    session: AsyncSession,
    repo: TodoItemRepository,
):
    with pytest.raises(repo_exceptions.NotFound):
        await repo.get_one(999999)


async def test_get_one(session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(
        title="Test get_one",
        description="test get_one desc",
        is_completed=False,
    )
    session.add(item)
    await session.commit()

    item_from_db = await repo.get_one(item.id)
    assert vars(item) == vars(item_from_db)


async def test_get_one_or_none(session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(
        title="Test get_one_or_none",
        description="test get_one_or_none desc",
        is_completed=False,
    )
    session.add(item)
    await session.commit()

    item_from_db = await repo.get_one_or_none(item.id)
    assert vars(item) == vars(item_from_db)

    none_item_from_db = await repo.get_one_or_none(999999)
    assert none_item_from_db is None


async def test_list_(session: AsyncSession, repo: TodoItemRepository):
    items = [
        TodoItem(
            title=f"Test list {i}",
            description="test list",
            is_completed=False,
        )
        for i in range(100)
    ]

    session.add_all(items)
    await session.commit()

    items_from_db = await repo.list_(description="test list")
    assert len(items_from_db) == len(items)
    assert all((item.title in [i.title for i in items_from_db] for item in items))


async def test_list_and_count(session: AsyncSession, repo: TodoItemRepository):
    items = [
        TodoItem(
            title=f"Test list {i}",
            description="test list",
            is_completed=False,
        )
        for i in range(100)
    ]

    session.add_all(items)
    await session.commit()

    items_from_db, count = await repo.list_and_count(description="test list")
    assert len(items_from_db) == len(items)
    assert all((item.title in [i.title for i in items_from_db] for item in items))
    assert count == len(items)


async def test_update(session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(title="Test update", description="test update desc", is_completed=False)
    session.add(item)
    await session.commit()

    item.title = "Test update updated"
    await repo.update(item)

    item_from_db = (
        await session.execute(select(TodoItem).where(TodoItem.id == item.id))
    ).scalar_one_or_none()
    assert item_from_db is not None
    assert item_from_db.title == "Test update updated"


async def test_update_raises_not_found(session: AsyncSession, repo: TodoItemRepository):
    with pytest.raises(repo_exceptions.NotFound):
        await repo.update(TodoItem(id=123123123, title="title", is_completed=False))


async def test_update_many(session: AsyncSession, repo: TodoItemRepository):
    items = [
        TodoItem(title=f"Test update {i}", description="test update desc", is_completed=False)
        for i in range(10)
    ]
    session.add_all(items)
    await session.commit()

    for i, item in enumerate(items):
        item.title = f"Test update updated {i}"

    await repo.update_many(items)

    items_from_db = (
        (
            await session.execute(
                select(TodoItem).where(TodoItem.title.like("Test update updated%"))
            )
        )
        .scalars()
        .all()
    )

    assert len(items_from_db) == len(items)
    assert all((item.title in [i.title for i in items_from_db] for item in items))


async def test_upsert_create(session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(title="Test upsert", description="test upsert desc", is_completed=False)
    upserted = await repo.upsert(item)

    assert upserted.id

    item_from_db = (
        await session.execute(select(TodoItem).where(TodoItem.id == upserted.id))
    ).scalar_one_or_none()
    assert item_from_db is not None
    assert item_from_db.id == upserted.id


async def test_upsert_update(session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(title="Test upsert", description="test upsert desc", is_completed=False)
    session.add(item)
    await session.commit()

    item.title = "Test upsert updated"

    upserted = await repo.upsert(item)

    assert upserted == item
    assert upserted.title == "Test upsert updated"

    item_from_db = (
        await session.execute(select(TodoItem).where(TodoItem.id == upserted.id))
    ).scalar_one_or_none()
    assert item_from_db is not None
    assert item_from_db.title == "Test upsert updated"


async def test_upsert_many_create(session: AsyncSession, repo: TodoItemRepository):
    items = [
        TodoItem(title=f"Test upsert {i}", description="test upsert desc", is_completed=False)
        for i in range(10)
    ]

    upserted = await repo.upsert_many(items)
    assert len(upserted) == len(items)
    assert all((item.id for item in upserted))

    items_from_db = (
        (await session.execute(select(TodoItem).where(TodoItem.title.like("Test upsert%"))))
        .scalars()
        .all()
    )
    assert len(items_from_db) == len(items)


async def test_upsert_many_update(session: AsyncSession, repo: TodoItemRepository):
    items = [
        TodoItem(title=f"Test upsert {i}", description="test upsert desc", is_completed=False)
        for i in range(10)
    ]
    session.add_all(items)
    await session.commit()

    for item in items:
        item.title = "Test upsert updated"

    upserted = await repo.upsert_many(items)
    assert len(upserted) == len(items)

    items_from_db = (
        (await session.execute(select(TodoItem).where(TodoItem.title.like("Test upsert%"))))
        .scalars()
        .all()
    )
    assert len(items_from_db) == len(items)
    assert all((item.title == "Test upsert updated" for item in items_from_db))
