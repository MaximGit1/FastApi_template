from dataclasses import dataclass
from roles import RolePermission

@dataclass
class User:
    nickname: str
    id: int | None = None
    is_active: bool = True
    role: RolePermission = RolePermission.DEFAULT
