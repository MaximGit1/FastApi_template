from dataclasses import dataclass
from .roles import RolePermission


@dataclass
class User:
    nickname: str
    id: int | None = None
    is_active: bool | None = None
    is_super_user: bool | None = None
    role: RolePermission | str | None = None
    password: bytes | str | None = None
