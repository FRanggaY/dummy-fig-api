from app.dtos.user import UserCreate, UserEdit

user_mock = UserCreate(username="john_doe", email="john@example.com", password="secret")
user_edit_mock = UserEdit(username="hero_john_doe", email="john123@example.com", status="active")
