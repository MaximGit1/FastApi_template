from dataclasses import dataclass
from typing import NewType


AccessToken = NewType("AccessToken", str)
RefreshToken = NewType("RefreshToken", str)


@dataclass
class TokenData:
    access_token: AccessToken
    refresh_token: RefreshToken | None
    token_type: str = "Bearer"
