from typing import Protocol
from abc import abstractmethod

from src.domain.models import User


class UserReader(Protocol):
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None: ...

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    async def get_all_users(self) -> list[User]: ...
