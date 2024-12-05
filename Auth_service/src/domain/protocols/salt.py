from abc import abstractmethod
from typing import Protocol


class SaltProtocol(Protocol):
    @abstractmethod
    def hash_password(self, password: str) -> bytes: ...

    @abstractmethod
    def validate_password(
        self, password: str, hashed_password: bytes
    ) -> bool: ...
