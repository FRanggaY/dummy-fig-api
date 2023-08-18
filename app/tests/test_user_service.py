from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.main import app
from app.models.user import User
from app.services.user_service import UserService
from app.data_mock.user_mock import user_mock, user_edit_mock

client = TestClient(app)

def test_create_user(db: Session = next(get_db())):
    user_service = UserService(db)
    username_test = "john_doe"
    created_user = user_service.create_user(user_mock)
    assert created_user.username == username_test
    assert db.query(User).filter(User.username == username_test).first() is not None

def test_read_all_user_exist(db: Session = next(get_db())):
    user_service = UserService(db)
    userstatus = "all"
    users = user_service.read_all_user(userstatus)
    assert users is not None

def test_update_user_exist(db: Session = next(get_db())):
    user_service = UserService(db)
    username_test = "john_doe"
    new_username_test = "hero_john_doe"
    new_email_test = "john123@example.com"
    new_status_test = "active"
    user_id = db.query(User.id).filter(User.username == username_test).scalar()
    user = user_service.update_user(user_edit_mock, user_id)
    assert user.username == new_username_test
    assert user.email == new_email_test
    assert user.status == new_status_test

def test_delete_user_exist(db: Session = next(get_db())):
    user_service = UserService(db)
    username_test = "hero_john_doe"
    user_id = db.query(User.id).filter(User.username == username_test).scalar()
    user = user_service.delete_user(user_id)
    assert user is not None
