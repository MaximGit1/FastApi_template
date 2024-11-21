from typing import Protocol
from abc import abstractmethod

from src.domain.models import AccessToken, RefreshToken, TokenData, User


class JWTGenerator(Protocol):
    @abstractmethod
    def create_token(
        self, user: User, token_type: AccessToken | RefreshToken
    ) -> TokenData: ...

    @abstractmethod
    def decode_token(self, token: TokenData) -> dict: ...

    @abstractmethod
    async def validate_token(self, user_id: int, token: TokenData) -> bool: ...

    @abstractmethod
    def get_token_payload(self, token: TokenData) -> dict: ...
