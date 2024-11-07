from abc import abstractmethod
from typing import Protocol

from src.domain.models import UserDomain


class UserProtocol(Protocol):
    @abstractmethod
    async def get_all(self) -> list[UserDomain]: ...

    @abstractmethod
    async def get_by_id(self, user_id: int) -> UserDomain | None: ...

    @abstractmethod
    async def create(self, user: UserDomain) -> UserDomain: ...

    @abstractmethod
    async def update(self, user: UserDomain) -> bool: ...

    @abstractmethod
    async def delete_by_id(self, user_id: int) -> None: ...
