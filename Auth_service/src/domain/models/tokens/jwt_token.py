from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from enum import Enum

from src.domain.models.users.user import UserID

Token = NewType("Token", str)


class TokenTypes(Enum):
    AccessToken = "access"
    RefreshToken = "refresh"


@dataclass
class TokenBase:
    token: Token
    token_type: TokenTypes | None

    def __str__(self):
        return self.token


class AccessToken(TokenBase):
    def __init__(self, token: Token):
        super().__init__(token=token, token_type=TokenTypes.AccessToken.value)


class RefreshToken(TokenBase):
    def __init__(self, token: Token):
        super().__init__(token=token, token_type=TokenTypes.RefreshToken.value)


@dataclass
class AccessPayload:
    sub: UserID

    exp: datetime | None = None
    token_type: TokenTypes = TokenTypes.AccessToken.value
