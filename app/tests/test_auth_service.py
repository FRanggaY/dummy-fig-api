from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.main import app
from app.models.user import User
from app.services.auth_service import AuthService
from app.data_mock.auth_mock import auth_login_mock, auth_login_not_exist_mock, auth_login_wrong_password_mock


client = TestClient(app)

def test_auth_login_success(db: Session = next(get_db())):
    auth_service = AuthService(db)
    username_test = "john_doe"

    user_id = db.query(User.id).filter(User.username == username_test).scalar()

    ## NOTES : comment test_user_service on update and delete test

    auth_data = auth_service.auth_login(auth_login_mock)
    assert auth_data.get('user_id', None) == user_id
    assert auth_data.get('access_token', None) is not None
    assert auth_data.get('refresh_token', None) is not None
    assert auth_data.get('access_token_expired_at', None) is not None

def test_auth_login_not_exist(db: Session = next(get_db())):
    auth_service = AuthService(db)

    ## NOTES : comment test_user_service on update and delete test

    try:
        auth_service.auth_login(auth_login_not_exist_mock)
    except ValueError as error:
        assert str(error) == "Username not found"

def test_auth_login_wrong_password(db: Session = next(get_db())):
    auth_service = AuthService(db)

    ## NOTES : comment test_user_service on update and delete test

    try:
        auth_service.auth_login(auth_login_wrong_password_mock)
    except ValueError as error:
        assert str(error) == "Password invalid"
