from datetime import date
from fastapi.testclient import TestClient
from RacunPlus.main import app

client = TestClient(app)

def get_auth_token():
    client.post("/auth/register", json={
        "username": "transuser",
        "email": "transuser@example.com",
        "password": "pass123",
        "first_name": "Trans",
        "last_name": "User"
    })
    response = client.post("/auth/login", data={
        "username": "transuser",
        "password": "pass123"
    })
    return response.json()["access_token"]


def test_1_create_transaction():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/transactions/create", json={
        "amount": 50.0,
        "merchant_name": "Market",
        "transaction_date": str(date.today()),
        "status": "completed"
    }, headers=headers)
    
    print(f"Create transaction: {response.status_code}")
    assert response.status_code == 201


def test_2_list_transactions():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/transactions/list", headers=headers)
    print(f"List transactions: {response.status_code}")
    assert response.status_code == 200


def test_3_transaction_bez_auth():
    response = client.get("/transactions/list")
    print(f"Without auth: {response.status_code}")
    assert response.status_code in [401, 403]
