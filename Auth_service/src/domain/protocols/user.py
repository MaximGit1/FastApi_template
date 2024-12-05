from abc import abstractmethod
from typing import Protocol

from src.domain.models import User, UserID, UserData


class UserDAOProtocol(Protocol):
    @abstractmethod
    async def create_user(self, user_data: UserData) -> UserID: ...

    @abstractmethod
    async def get_user_by_id(self, user_id: UserID) -> User | None: ...

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    async def get_all_users(self) -> list[User]: ...

    @abstractmethod
    async def get_user_all_data_by_username(
        self, username: str
    ) -> User | None: ...
