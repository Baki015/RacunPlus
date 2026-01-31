from fastapi.testclient import TestClient
from RacunPlus.main import app
import uuid

client = TestClient(app)

def test_1_register():
    unique_id = uuid.uuid4().hex[:8]
    response = client.post("/auth/register", json={
        "username": f"testuser_{unique_id}",
        "email": f"test_{unique_id}@example.com",
        "password": "pass123",
        "first_name": "Test",
        "last_name": "User"
    })
    print(f"Register response: {response.status_code}")
    assert response.status_code == 201


def test_2_login():
    client.post("/auth/register", json={
        "username": "testuser1",
        "email": "test1@example.com",
        "password": "pass123",
        "first_name": "Test",
        "last_name": "User"
    })
    response = client.post("/auth/login", data={
        "username": "testuser1",
        "password": "pass123"
    })
    print(f"Login response: {response.status_code}")
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_3_login_pogresan():
    response = client.post("/auth/login", data={
        "username": "testuser1",
        "password": "pogresna"
    })
    print(f"Wrong password response: {response.status_code}")
    assert response.status_code == 401