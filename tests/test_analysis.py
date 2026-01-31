from datetime import date
from fastapi.testclient import TestClient
from RacunPlus.main import app

client = TestClient(app)

def get_auth_token():
    client.post("/auth/register", json={
        "username": "analysisuser",
        "email": "analysisuser@example.com",
        "password": "pass123",
        "first_name": "Analysis",
        "last_name": "User"
    })
    response = client.post("/auth/login", data={
        "username": "analysisuser",
        "password": "pass123"
    })
    return response.json()["access_token"]


def test_1_generate_monthly_analysis():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    client.post("/bills/create", json={
        "amount": 100.0,
        "beneficiary_name": "EPS",
        "reference_date": str(date.today()),
        "status": "paid"
    }, headers=headers)
    
    response = client.post("/analysis/generate", json={
        "analysis_type": "monthly",
        "days": 30
    }, headers=headers)
    
    print(f"Generate analysis: {response.status_code}")
    assert response.status_code in [201, 429]


def test_2_generate_category_analysis():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    client.post("/bills/create", json={
        "amount": 50.0,
        "beneficiary_name": "Internet",
        "reference_date": str(date.today()),
        "status": "paid"
    }, headers=headers)
    
    response = client.post("/analysis/generate", json={
        "analysis_type": "category",
        "days": 30
    }, headers=headers)
    
    print(f"Category analysis: {response.status_code}")
    assert response.status_code in [201, 429]


def test_3_analysis_bez_auth():
    response = client.post("/analysis/generate", json={
        "analysis_type": "monthly",
        "days": 30
    })
    print(f"Without auth: {response.status_code}")
    assert response.status_code in [401, 403]
