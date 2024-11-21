from abc import abstractmethod
from typing import Protocol

from src.domain.models import User


class UserCreatorProtocol(Protocol):
    @abstractmethod
    async def create_user(
        self, username: str, email: str, password: str
    ) -> User: ...
