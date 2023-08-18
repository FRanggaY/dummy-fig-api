from sqlalchemy.orm import Session
from app.dtos.user import UserCreate, UserEdit
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.password_service import PasswordService

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def create_user(self, user_create: UserCreate):
        hashed_password = PasswordService.hash_password(user_create.password)
        user_model = User(username=user_create.username, email=user_create.email, hashed_password=hashed_password)
        return self.user_repository.create_user(user_model)

    def check_username_exists(self, username: str):
        if self.user_repository.get_user_by_username(username):
            raise ValueError("Username already exists")

    def check_email_exists(self, email: str):
        if self.user_repository.get_user_by_email(email):
            raise ValueError("Email already exists")

    def read_all_user(self, user_status: str):
        user_datas = []
        users = self.user_repository.read_all_user(user_status)
        if len(users) > 0:
            for user in users:
                user_datas.append(
                    {
                        'id': user.id,
                        'username': user.username,
                        'status': user.status,
                    }
                )
        return user_datas

    def update_user(self, user_edit: UserEdit, id: str):
        user = self.user_repository.read_user(id)
        if user:
            if user_edit.username:
                user.username = user_edit.username
            if user_edit.email:
                user.email = user_edit.email
            if user_edit.status:
                user.status = user_edit.status
            if user_edit.password:
                hashed_password = PasswordService.hash_password(user_edit.password)
                user.hashed_password = hashed_password
            return self.user_repository.update_user(user)
        else:
            return ''

    def read_user(self, id: str):
        user = self.user_repository.read_user(id)
        return user

    def delete_user(self, id: str):
        user_id = self.user_repository.delete_user(id)
        return user_id
