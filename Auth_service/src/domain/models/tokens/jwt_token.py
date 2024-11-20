from dataclasses import dataclass
from typing import NewType
from enum import StrEnum


class TokenTypes(StrEnum):
    Access = "access"
    Refresh = "refresh"


AccessToken = NewType("AccessToken", str)
RefreshToken = NewType("RefreshToken", str)


@dataclass
class TokenData:
    token: str
    token_type: TokenTypes

    @classmethod
    def from_access(cls, token: str) -> "TokenData":
        return cls(token=token, token_type=TokenTypes.Access)

    @classmethod
    def from_refresh(cls, token: str) -> "TokenData":
        return cls(token=token, token_type=TokenTypes.Refresh)


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: str