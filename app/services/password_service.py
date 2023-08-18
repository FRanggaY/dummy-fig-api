from werkzeug.security import generate_password_hash, check_password_hash

class PasswordService:
    @staticmethod
    def hash_password(password: str) -> str:
        return generate_password_hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return check_password_hash(hashed_password, plain_password)
