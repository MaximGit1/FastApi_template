from src.domain.protocols import SaltProtocol


class SaltService:
    def __init__(
        self,
        salt_repository: SaltProtocol,
    ) -> None:
        self._salt_repository = salt_repository

    def hash_password(self, password: str) -> bytes:
        return self._salt_repository.hash_password(password=password)

    def validate_password(self, password: str, hashed_password: bytes) -> bool:
        return self._salt_repository.validate_password(
            password=password, hashed_password=hashed_password
        )
