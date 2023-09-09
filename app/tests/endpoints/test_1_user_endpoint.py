from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.main import app
from app.models.user import User
from app.data_mock.user_mock import user_mock
from app.tests.endpoints import handle_data_user

client = TestClient(app)

def test_create_user(db: Session = next(get_db())):
    # Perform the creation
    response = client.post("/api/v1/users", json=user_mock)
    assert response.status_code == 201

    # Verify that the username is not exist
    assert db.query(User).filter(User.username == user_mock.get('username')).first() is not None, f"{user_mock.get('username')} still exists in the database"

    # Verify that the email is not exist
    assert db.query(User).filter(User.email == user_mock.get('email')).first() is not None, f"{user_mock.get('email')} still exists in the database"

def test_create_user_exist():
    # Perform the creation
    response = client.post("/api/v1/users", json=user_mock)
    assert response.status_code == 400

def test_read_all_user():
    # Perform the reading
    response = client.get("/api/v1/users?user_status=all")
    data = response.json()
    handle_data_user(response, data, 'multiple')

    # Perform the reading
    response = client.get("/api/v1/users?user_status=idle")
    data = response.json()
    handle_data_user(response, data, 'multiple')

