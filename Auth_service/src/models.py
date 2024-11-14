from dataclasses import dataclass
from typing import NewType


AccessToken = NewType("JWT", str)
RefreshToken = NewType("RefreshToken", str)


@dataclass
class User:
    username: str
    password: str | bytes
    id: int | None = None
    is_active: bool = True


@dataclass
class TokenData:
    access_token: AccessToken
    refresh_token: RefreshToken
    token_type: str = "Bearer"
