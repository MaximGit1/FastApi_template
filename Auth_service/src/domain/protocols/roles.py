from abc import abstractmethod
from typing import Protocol

from src.domain.models import Role


class RoleProtocol(Protocol):
    @abstractmethod
    def from_user(self, role: Role) -> bool: ...

    @abstractmethod
    def from_employee(self, role: Role) -> bool: ...

    @abstractmethod
    def from_admin(self, role: Role) -> bool: ...

    @abstractmethod
    def is_super_user(self, role: Role) -> bool: ...
