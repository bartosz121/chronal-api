import httpx


async def test_index(
    client: httpx.AsyncClient,
):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "ok"}
