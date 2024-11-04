from abc import abstractmethod
from typing import Protocol, NewType

from src.domain.models import UserDomain, GlobalPermissionDomain


JWT_TOKEN = NewType("JWT_TOKEN", str)


class UserProtocol(Protocol):
    @abstractmethod
    async def register_user(
        self, nickname: str, password: str
    ) -> UserDomain: ...

    @abstractmethod
    async def authenticate_user(
        self, nickname: str, password: str
    ) -> JWT_TOKEN: ...

    @abstractmethod
    async def verify_token(self, token: JWT_TOKEN) -> UserDomain | None: ...

    @abstractmethod
    async def check_permission(
        self, user: UserDomain, permission: GlobalPermissionDomain
    ) -> bool: ...
