from typing import Protocol
from abc import abstractmethod

from src.domain.models import User, Roles


class UserSaver(Protocol):
    @abstractmethod
    async def create_user(
        self, username: str, email: str, password: str
    ) -> User: ...
