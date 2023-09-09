import uuid
from sqlalchemy.orm import Session
from app.models.user import User, UserStatusParamCustom

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User):
        user.id = str(uuid.uuid4())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def read_all_user(self, user_status: str) -> User:
        if user_status == UserStatusParamCustom.all:
            users = self.db.query(User.id, User.username, User.status).all()
        else:
            users = self.db.query(User.id, User.username, User.status).filter(User.status == user_status).all()
        return users

    def update_user(self, user: User):
        self.db.commit()
        return user

    def read_user(self, id: str) -> User:
        user = self.db.query(User).filter(User.id == id).first()
        return user

    def delete_user(self, id: str) -> str:
        user = self.db.query(User).filter(User.id == id).first()
        if user:
            user_id = user.id
            self.db.delete(user)
            self.db.commit()
            return user_id
        else:
            return ''

