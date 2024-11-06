from dataclasses import dataclass
from roles import RolePermission


@dataclass
class User:
    nickname: str
    id: int | None = None
    is_active: bool = True
    is_super_user: bool = False
    role: RolePermission | None = None
    password: bytes | str | None = None
