import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import base64

import pytest
from httpx import AsyncClient, ASGITransport

from api.main import app


VALID_USER = "test"
VALID_PASSWORD = "1234"
INVALID_PASSWORD = "5678"

def basic_auth_header(username, password):
    """
    Authentication information.

    :param username: login
    :type username: str
    :param password: password
    :type password: str
    """
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}

@pytest.mark.asyncio
async def test_get_users_unauthenticated():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/users/")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_search_users_unauthenticated():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/users/q=gigle")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_user_unauthenticated():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/users/giglestudios")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_users_authenticated():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as ac:
        headers = basic_auth_header(VALID_USER, VALID_PASSWORD)
        response = await ac.get("/users/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "id" in data[0]
    assert "login" in data[0]
    assert isinstance(data[0]["id"], int)
    assert isinstance(data[0]["login"], str)

@pytest.mark.asyncio
async def test_search_users_authenticated():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as ac:
        headers = basic_auth_header(VALID_USER, VALID_PASSWORD)
        response = await ac.get("/users/search?q=gigle", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "id" in data[0]
    assert "login" in data[0]
    assert isinstance(data[0]["id"], int)
    assert isinstance(data[0]["login"], str)

@pytest.mark.asyncio
async def test_get_user_authenticated():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as ac:
        headers = basic_auth_header(VALID_USER, VALID_PASSWORD)
        response = await ac.get("/users/giglestudios", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "id" in data
    assert "login" in data
    assert "created_at" in data
    assert "avatar_url" in data
    assert "bio" in data
    assert isinstance(data["id"], int)
    assert isinstance(data["login"], str)
    assert isinstance(data["created_at"], str)
    assert isinstance(data["avatar_url"], str)
    assert isinstance(data["bio"], str)