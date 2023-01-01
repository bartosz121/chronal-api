import pytest
from httpx import AsyncClient

from .data import AUTH_CLIENT_SUPERUSER, AUTH_CLIENT_USER0, user_objs


@pytest.mark.asyncio
async def test_me_get_no_auth_returns_401(client: AsyncClient):
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


@pytest.mark.asyncio
async def test_me_get(user0_client: AsyncClient):
    response = await user0_client.get("/api/v1/users/me")
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == AUTH_CLIENT_USER0["email"]
    assert data["first_name"] == AUTH_CLIENT_USER0["first_name"]
    assert data["last_name"] == AUTH_CLIENT_USER0["last_name"]
    assert data["timezone"] == AUTH_CLIENT_USER0["timezone"]


@pytest.mark.asyncio
async def test_me_patch(user2_client: AsyncClient):
    data = {
        "email": "PATCHEDemail@example.com",
        "timezone": "Australia/Currie",
        "first_name": "PATCHED first name",
        "last_name": "PATCHED last name",
    }

    response = await user2_client.patch("/api/v1/users/me", json=data)
    assert response.status_code == 200

    data_patched = response.json()
    assert data_patched["email"] == data["email"]
    assert data_patched["timezone"] == data["timezone"]
    assert data_patched["first_name"] == data["first_name"]
    assert data_patched["last_name"] == data["last_name"]


@pytest.mark.asyncio
async def test_get_by_id_no_superuser_returns_403(user0_client: AsyncClient):
    response = await user0_client.get(f"/api/v1/users/{user_objs[3]['id']}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"


@pytest.mark.asyncio
async def test_get_by_id(superuser_client: AsyncClient):
    target_user = user_objs[3]
    response = await superuser_client.get(f"/api/v1/users/{target_user['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == target_user["id"]


@pytest.mark.asyncio
async def test_patch_by_id_no_superuser_returns_403(user0_client: AsyncClient):
    target_user = user_objs[3]
    response = await user0_client.patch(f"/api/v1/users/{target_user['id']}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"


@pytest.mark.asyncio
async def test_patch_by_id_does_not_exist_404(superuser_client: AsyncClient):
    random_id = "e6549a0a-1681-4f85-a071-e970e075a0f3"
    r_exists = await superuser_client.patch(f"/api/v1/users/{random_id}")
    assert r_exists.status_code == 404
    assert r_exists.json()["detail"] == "Not Found"


@pytest.mark.asyncio
async def test_patch_by_id(superuser_client: AsyncClient):
    target_user_id = user_objs[3]["id"]
    patch_data = {
        "first_name": "patch first name",
        "last_name": "patch last name",
        "timezone": "Etc/UTC",
    }

    response = await superuser_client.patch(
        f"/api/v1/users/{target_user_id}", json=patch_data
    )

    assert response.status_code == 200

    patched_data = response.json()
    assert patched_data["first_name"] == patch_data["first_name"]
    assert patched_data["last_name"] == patch_data["last_name"]
    assert patched_data["timezone"] == patch_data["timezone"]


@pytest.mark.asyncio
async def test_delete_by_id_no_superuser_returns_403(user0_client: AsyncClient):
    response = await user0_client.delete(f"/api/v1/users/{user_objs[3]['id']}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"


@pytest.mark.asyncio
async def test_delete_by_id_does_not_exist_404(superuser_client: AsyncClient):
    random_id = "da99b4e3-2c7b-44c7-a90f-d26989884f6e"
    r_exists = await superuser_client.get(f"/api/v1/users/{random_id}")
    assert r_exists.status_code == 404
    assert r_exists.json()["detail"] == "Not Found"


@pytest.mark.asyncio
async def test_delete_by_id(superuser_client: AsyncClient):
    target_user = user_objs[3]
    r_exists = await superuser_client.get(f"/api/v1/users/{target_user['id']}")
    assert r_exists.status_code == 200

    r_delete = await superuser_client.delete(f"/api/v1/users/{target_user['id']}")
    assert r_delete.status_code == 204

    r_does_not_exist = await superuser_client.get(f"/api/v1/users/{target_user['id']}")
    assert r_does_not_exist.status_code == 404
    assert r_does_not_exist.json()["detail"] == "Not Found"
