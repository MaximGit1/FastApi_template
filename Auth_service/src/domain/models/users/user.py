from dataclasses import dataclass

from .roles import Roles

@dataclass
class User:
    username: str | None
    id: int | None = None
    email: str | None = None
    hashed_password: bytes | None = None
    role: Roles | None = None
    is_active: bool | None = True
    is_super_user: bool | None = False
