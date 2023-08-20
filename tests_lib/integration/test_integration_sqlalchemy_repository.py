import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from chronal_api.lib.repository import exceptions as repo_exceptions
from chronal_api.lib.repository.sqlalchemy import SQLAlchemyRepository

from ..conftest import DUMMY_COUNT
from ..model import TodoItem


class TodoItemRepository(SQLAlchemyRepository[TodoItem, int]):
    model = TodoItem


@pytest.fixture(scope="function")
async def repo(db_session) -> SQLAlchemyRepository[TodoItem, int]:
    return TodoItemRepository(db_session)


async def test_count(repo: TodoItemRepository):
    repo_count = await repo.count()
    assert repo_count == DUMMY_COUNT


async def test_count_kwargs(db_session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(
        title="Test count kwargs",
        description="test count kwargs desc",
        is_complete=False,
    )
    db_session.add(item)
    await db_session.commit()

    repo_count = await repo.count(
        title=item.title,
        description=item.description,
        is_complete=item.is_complete,
    )
    assert repo_count == 1


async def test_create(db_session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(
        title="Test create",
        description="test create desc",
        is_complete=False,
    )
    created = await repo.create(item)
    assert created == item
    assert created.id

    item_from_db = (
        await db_session.execute(select(TodoItem).where(TodoItem.title == "Test create"))
    ).scalar_one_or_none()
    assert item_from_db is not None
    assert item_from_db.id == created.id


async def test_create_many(db_session: AsyncSession, repo: TodoItemRepository):
    items = [
        TodoItem(
            title=f"Test create_many {i}",
            description=f"test create_many {i}",
            is_complete=False,
        )
        for i in range(10)
    ]

    created = await repo.create_many(items)
    assert created == items
    assert all((item.id for item in created))

    items_from_db = (
        (await db_session.execute(select(TodoItem).where(TodoItem.title.like("Test create_many%")))).scalars().all()
    )

    assert len(items_from_db) == len(items)
    assert all((item.id in [i.id for i in items_from_db] for item in items))


async def test_delete(db_session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(
        title="Test delete",
        description="test delete desc",
        is_complete=False,
    )
    db_session.add(item)
    await db_session.commit()

    deleted = await repo.delete(item.id)
    assert deleted == item

    should_be_none = (await db_session.execute(select(TodoItem).where(TodoItem.id == item.id))).scalar_one_or_none()
    assert should_be_none is None


# Check your sqlite version if this fails, delete_many uses `RETURNING` which is supported in 3.35.0+
async def test_delete_many(db_session: AsyncSession, repo: TodoItemRepository):
    items = [
        TodoItem(
            title=f"Test delete_many {i}",
            description=f"test delete_many {i}",
            is_complete=False,
        )
        for i in range(10)
    ]

    db_session.add_all(items)
    await db_session.commit()

    deleted = await repo.delete_many([item.id for item in items])
    assert len(deleted) == len(items)
    assert all((item.title in [i.title for i in deleted] for item in items))

    items_from_db = (
        (await db_session.execute(select(TodoItem).where(TodoItem.title.like("Test delete_many%")))).scalars().all()
    )
    assert items_from_db == []


async def test_exists(db_session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(
        title="Test exists",
        description="test exists desc",
        is_complete=False,
    )
    db_session.add(item)
    await db_session.commit()

    assert (await repo.exists(id=item.id)) is True
    assert (await repo.exists(title=item.title)) is True
    assert (await repo.exists(description=item.description)) is True


async def test_exists_false(repo: TodoItemRepository):
    assert (await repo.exists(id=999999)) is False
    assert (await repo.exists(title="Test exists")) is False
    assert (await repo.exists(description="test exists desc")) is False


async def test_get(db_session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(
        title="Test get",
        description="test get desc",
        is_complete=False,
    )
    db_session.add(item)
    await db_session.commit()

    item_from_db = await repo.get(item.id)
    assert vars(item) == vars(item_from_db)


async def test_get_raises_not_found(repo: TodoItemRepository):
    with pytest.raises(repo_exceptions.NotFoundError):
        await repo.get(999999)


async def test_get_one_raises_not_found(
    db_session: AsyncSession,
    repo: TodoItemRepository,
):
    with pytest.raises(repo_exceptions.NotFoundError):
        await repo.get_one(999999)


async def test_get_one(db_session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(
        title="Test get_one",
        description="test get_one desc",
        is_complete=False,
    )
    db_session.add(item)
    await db_session.commit()

    item_from_db = await repo.get_one(item.id)
    assert vars(item) == vars(item_from_db)


async def test_get_one_or_none(db_session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(
        title="Test get_one_or_none",
        description="test get_one_or_none desc",
        is_complete=False,
    )
    db_session.add(item)
    await db_session.commit()

    item_from_db = await repo.get_one_or_none(item.id)
    assert vars(item) == vars(item_from_db)

    none_item_from_db = await repo.get_one_or_none(999999)
    assert none_item_from_db is None


async def test_list_(db_session: AsyncSession, repo: TodoItemRepository):
    items = [
        TodoItem(
            title=f"Test list {i}",
            description="test list",
            is_complete=False,
        )
        for i in range(100)
    ]

    db_session.add_all(items)
    await db_session.commit()

    items_from_db = await repo.list_(description="test list")
    assert len(items_from_db) == len(items)
    assert all((item.title in [i.title for i in items_from_db] for item in items))


async def test_list_and_count(db_session: AsyncSession, repo: TodoItemRepository):
    items = [
        TodoItem(
            title=f"Test list {i}",
            description="test list",
            is_complete=False,
        )
        for i in range(100)
    ]

    db_session.add_all(items)
    await db_session.commit()

    items_from_db, count = await repo.list_and_count(description="test list")
    assert len(items_from_db) == len(items)
    assert all((item.title in [i.title for i in items_from_db] for item in items))
    assert count == len(items)


async def test_update(db_session: AsyncSession, repo: TodoItemRepository):
    assert True


async def test_update_many(db_session: AsyncSession, repo: TodoItemRepository):
    assert True


async def test_upsert_create(db_session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(title="Test upsert", description="test upsert desc", is_complete=False)
    upserted = await repo.upsert(item)

    assert upserted.id

    item_from_db = (await db_session.execute(select(TodoItem).where(TodoItem.id == upserted.id))).scalar_one_or_none()
    assert item_from_db is not None
    assert item_from_db.id == upserted.id


async def test_upsert_update(db_session: AsyncSession, repo: TodoItemRepository):
    item = TodoItem(title="Test upsert", description="test upsert desc", is_complete=False)
    db_session.add(item)
    await db_session.commit()

    item.title = "Test upsert updated"

    upserted = await repo.upsert(item)

    assert upserted == item
    assert upserted.title == "Test upsert updated"

    item_from_db = (await db_session.execute(select(TodoItem).where(TodoItem.id == upserted.id))).scalar_one_or_none()
    assert item_from_db is not None
    assert item_from_db.title == "Test upsert updated"


async def test_upsert_many_create(db_session: AsyncSession, repo: TodoItemRepository):
    items = [TodoItem(title=f"Test upsert {i}", description="test upsert desc", is_complete=False) for i in range(10)]

    upserted = await repo.upsert_many(items)
    assert len(upserted) == len(items)
    assert all((item.id for item in upserted))

    items_from_db = (
        (await db_session.execute(select(TodoItem).where(TodoItem.title.like("Test upsert%")))).scalars().all()
    )
    assert len(items_from_db) == len(items)


async def test_upsert_many_update(db_session: AsyncSession, repo: TodoItemRepository):
    items = [TodoItem(title=f"Test upsert {i}", description="test upsert desc", is_complete=False) for i in range(10)]
    db_session.add_all(items)
    await db_session.commit()

    for item in items:
        item.title = "Test upsert updated"

    upserted = await repo.upsert_many(items)
    assert len(upserted) == len(items)

    items_from_db = (
        (await db_session.execute(select(TodoItem).where(TodoItem.title.like("Test upsert%")))).scalars().all()
    )
    assert len(items_from_db) == len(items)
    assert all((item.title == "Test upsert updated" for item in items_from_db))
