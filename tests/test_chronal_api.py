import pytest
from httpx import AsyncClient

from chronal_api import __version__
from chronal_api.core.config import get_config

config = get_config()


def test_version():
    assert __version__ == "0.1.0"


@pytest.mark.asyncio
async def test_home(client: AsyncClient):
    response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {"msg": config.TITLE}
