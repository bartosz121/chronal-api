from unittest import mock

import pytest

from chronal_api.lib.repository import Repository
from chronal_api.lib.service import Service


@pytest.fixture
def service() -> Service:
    return Service(mock.AsyncMock(spec=Repository))


def test_service_init():
    repository = mock.Mock(spec=Repository)
    service = Service(repository)

    assert service.repository == repository


async def test_service_count(service: Service):
    data = {"a": 1}

    await service.count(**data)
    service.repository.count.assert_called_once_with(**data)


async def test_service_create(service: Service):
    data = {"test": 1}
    await service.create(data)

    service.repository.create.assert_called_once_with(data)


async def test_service_create_many(service: Service):
    data = [{"test_1": 1}, {"test_2": 2}]
    await service.create_many(data)

    service.repository.create_many.assert_called_once_with(data)


async def test_service_delete(service: Service):
    id_ = 10
    await service.delete(id_)

    service.repository.delete.assert_called_once_with(id_)


async def test_service_delete_many(service: Service):
    ids = [1, 2]
    await service.delete_many(ids)

    service.repository.delete_many.assert_called_once_with(ids)


async def test_service_exists(service: Service):
    data = {"test": 1}

    await service.exists(**data)

    service.repository.exists.assert_called_once_with(**data)


async def test_service_get(service: Service):
    id = 10
    await service.get(10)

    service.repository.get.assert_called_once_with(id)


async def test_service_get_one(service: Service):
    id_ = 10
    await service.get_one(id_)

    service.repository.get_one.assert_called_once_with(id_)


async def test_service_get_one_or_none(service: Service):
    id_ = 10
    await service.get_one_or_none(id_)

    service.repository.get_one_or_none.assert_called_once_with(id_)


async def test_service_list_(service: Service):
    data = {"test": 1}

    await service.list_(**data)

    service.repository.list_.assert_called_once_with(**data)


async def test_service_list_and_count(service: Service):
    data = {"test": 1}

    await service.list_and_count(**data)

    service.repository.list_and_count.assert_called_once_with(**data)


async def test_service_update(service: Service):
    data = {"test": 1}

    await service.update(data)

    service.repository.update.assert_called_once_with(data)


async def test_service_update_many(service: Service):
    data = [{"test_1": 1}, {"test_2": 2}]
    await service.update_many(data)

    service.repository.update_many.assert_called_once_with(data)


async def test_service_upsert(service: Service):
    data = {"test": 1}
    await service.upsert(data)

    service.repository.upsert.assert_called_once_with(data)


async def test_service_upsert_many(service: Service):
    data = [{"test_1": 1}, {"test_2": 2}]
    await service.upsert_many(data)

    service.repository.upsert_many.assert_called_once_with(data)
