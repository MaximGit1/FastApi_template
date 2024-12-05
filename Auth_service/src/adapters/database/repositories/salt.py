from bcrypt import gensalt, hashpw, checkpw

from src.domain.protocols import SaltProtocol


class SaltRepository(SaltProtocol):
    def hash_password(self, password: str) -> bytes:
        return hashpw(
            password=password.encode(),
            salt=gensalt(),
        )

    def validate_password(self, password: str, hashed_password: bytes) -> bool:
        return checkpw(
            password=password.encode(), hashed_password=hashed_password
        )
