from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.main import app
from app.models.user import User
from app.data_mock.auth_mock import auth_login_mock, auth_login_not_exist_mock, auth_login_wrong_password_mock

client = TestClient(app)

base_api_url = "/api/v1/auth/login"

def test_auth_login():
    # Perform the reading
    response = client.post(base_api_url, json=auth_login_mock)
    assert response.status_code == 200

    data = response.json()

    assert data['data']['access_token'] is not None

def test_auth_login_not_exist():
    # Perform the reading
    response = client.post(base_api_url, json=auth_login_not_exist_mock)
    assert response.status_code == 400

def test_auth_login_wrong_password():
    # Perform the reading
    response = client.post(base_api_url, json=auth_login_wrong_password_mock)
    assert response.status_code == 400



