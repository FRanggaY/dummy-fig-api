from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.main import app
from app.models.user import User
from app.data_mock.user_mock import user_mock, user_edit_mock
from app.tests.endpoints import handle_data_user

client = TestClient(app)

def test_read_user(db: Session = next(get_db())):
    # Check if the user exists before attempting deletion
    user_exist = db.query(User).filter(User.username == user_mock.get('username')).first()
    assert user_exist is not None, f"User {user_mock.get('username')} does not exist in the database"

    # Perform the reading
    response = client.get(f"/api/v1/users/{user_exist.id}")
    data = response.json()
    handle_data_user(response, data, 'single')

def test_update_user(db: Session = next(get_db())):
    # Check if the user exists before attempting deletion
    user_exist = db.query(User).filter(User.username == user_mock.get('username')).first()
    assert user_exist is not None, f"User {user_mock.get('username')} does not exist in the database"

    # Perform the reading
    response = client.patch(f"/api/v1/users/{user_exist.id}", json=user_edit_mock)
    assert response.status_code == 200

def test_delete_user(db: Session = next(get_db())):
    # Check if the user exists before attempting deletion
    user_exist = db.query(User).filter(User.username == user_edit_mock.get('username')).first()
    assert user_exist is not None, f"User {user_edit_mock.get('username')} does not exist in the database"

    # Perform the deletion
    response = client.delete(f"/api/v1/users/{user_exist.id}")
    assert response.status_code == 200

    # Perform the after deletion to check data already deleted
    response = client.delete(f"/api/v1/users/{user_exist.id}")
    assert response.status_code == 404

    db.commit()



