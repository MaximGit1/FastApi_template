from abc import abstractmethod
from typing import Protocol

from src.domain.models import Roles


class UserUpdaterProtocol(Protocol):
    @abstractmethod
    async def update_user_role(self, user_id: int, role: Roles) -> bool: ...

    @abstractmethod
    async def deactivate_user(self, user_id: int) -> None: ...

    @abstractmethod
    async def activate_user(self, user_id: int) -> None: ...

    @abstractmethod
    async def change_password(
        self, new_password: str, old_password: bytes
    ) -> bool: ...

    @abstractmethod
    async def change_email(
        self, new_password: str, old_password: bytes
    ) -> bool: ...
