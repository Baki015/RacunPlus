from datetime import date
from fastapi.testclient import TestClient
from RacunPlus.main import app

client = TestClient(app)

def get_auth_token():
    client.post("/auth/register", json={
        "username": "billuser",
        "email": "billuser@example.com",
        "password": "pass123",
        "first_name": "Bill",
        "last_name": "User"
    })
    response = client.post("/auth/login", data={
        "username": "billuser",
        "password": "pass123"
    })
    return response.json()["access_token"]


def test_1_create_bill():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/bills/create", json={
        "amount": 100.0,
        "beneficiary_name": "EPS",
        "reference_date": str(date.today()),
        "status": "paid"
    }, headers=headers)
    
    print(f"Create bill: {response.status_code}")
    assert response.status_code == 201


def test_2_list_bills():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/bills/list", headers=headers)
    print(f"List bills: {response.status_code}")
    assert response.status_code == 200


def test_3_bill_bez_auth():
    response = client.get("/bills/list")
    print(f"Without auth: {response.status_code}")
    assert response.status_code in [401, 403]