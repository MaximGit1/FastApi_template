from dataclasses import dataclass

from roles import Roles


@dataclass
class User:
    username: str
    id: int | None = None
    email: str | None = None
    password_hash: str | None = None
    role: Roles | None = None
    is_active: bool | None = True
    is_super_user: bool | None = False
