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
    token: AccessToken | RefreshToken
    token_type: TokenTypes
