from sqlalchemy.orm import Session
from app.dtos.auth import AuthLogin
from app.models.user import User, UserStatusParam
from app.repositories.auth_repository import AuthRepository
from app.repositories.user_repository import UserRepository
from app.services.password_service import PasswordService

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
        self.auth_repository = AuthRepository(db)

    def auth_login(self, auth_login: AuthLogin):
        user = self.user_repository.get_user_by_username(auth_login.username)
        if user and user.status == UserStatusParam.active:
            is_password_valid = PasswordService.verify_password(auth_login.password, user.hashed_password)
            return self.auth_repository.auth_login(user, is_password_valid)
        else:
            raise ValueError("Username not found or inactive")
