from typing import Protocol
from abc import abstractmethod

from src.domain.models import FrogDomain


class FrogProtocol(Protocol):
    @abstractmethod
    async def get_all(self) -> list[FrogDomain]: ...

    @abstractmethod
    async def get_by_id(self, frog_id: int) -> FrogDomain | None: ...

    @abstractmethod
    async def create(self, frog: FrogDomain) -> FrogDomain: ...

    @abstractmethod
    async def update(self, frog: FrogDomain) -> bool: ...

    @abstractmethod
    async def delete_by_id(self, frog_id: int) -> None: ...
