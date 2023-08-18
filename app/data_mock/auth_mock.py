from app.dtos.auth import AuthLogin

auth_login_mock = AuthLogin(username="john_doe", password="secret")
auth_login_not_exist_mock = AuthLogin(username="xtinmenum", password="secret")
auth_login_wrong_password_mock = AuthLogin(username="john_doe", password="wrong_password")
