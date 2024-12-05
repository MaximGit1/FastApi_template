from abc import abstractmethod
from typing import Protocol

from starlette.requests import Request

from src.domain.models import UserID, Role


class IdentityProvider(Protocol):
    @abstractmethod
    def get_current_user_id(self, request: Request) -> UserID | None: ...

    @abstractmethod
    async def get_current_user_role(self, request: Request) -> Role | None: ...
