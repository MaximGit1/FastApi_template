import bcrypt

from src.domain.protocols import SaltProtocol


class SaltService(SaltProtocol):
    def hash_password(self, password: str) -> bytes:
        salt = bcrypt.gensalt()
        password_bytes: bytes = password.encode()
        return bcrypt.hashpw(password_bytes, salt)

    def validate_password(self, password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(
            password=password.encode(), hashed_password=hashed_password
        )
