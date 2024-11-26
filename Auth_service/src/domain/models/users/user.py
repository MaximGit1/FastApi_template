from dataclasses import dataclass
from typing import NewType

from .roles import Role


UserID = NewType("UserID", int)


@dataclass
class User:
    username: str | None
    id: UserID | None = None
    email: str | None = None
    hashed_password: bytes | None = None
    role: Role | None = None
    is_active: bool | None = True


@dataclass
class UserData:
    username: str | None
    email: str | None
    password: str
