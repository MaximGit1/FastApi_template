from typing import Protocol
from abc import abstractmethod

from src.domain.models import User, TokenData


class UserReaderProtocol(Protocol):
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None: ...

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    async def get_all_users(self) -> list[User]: ...

    @abstractmethod
    async def get_login_user_data_by_username(
        self, username: str
    ) -> User | None: ...

    # @abstractmethod
    # async def get_user_data_by_access_token(self, access_token: TokenData) -> User: ...