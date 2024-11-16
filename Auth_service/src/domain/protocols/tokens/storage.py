from abc import abstractmethod
from typing import Protocol

from src.domain.models import TokenData


class JWTStorager(Protocol):
    @abstractmethod
    def save_token(self, user_id: int, token: TokenData) -> None:
        """Stores the token in the browser cache"""
        pass

    @abstractmethod
    def verify_token(self, token: str) -> bool:
        """Checks if the token is active"""
        pass

    @abstractmethod
    def delete_token(self, token: str) -> None:
        """Removes a token from the browser cache when the user logs out"""
        pass
