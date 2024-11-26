from typing import Protocol
from abc import abstractmethod

from src.domain.models import AccessPayload, AccessToken, RefreshToken


class JWTProtocol(Protocol):
    @abstractmethod
    def generate_access_token(self, payload: AccessPayload) -> AccessToken: ...

    # @abstractmethod
    # def generate_refresh_token(self) -> RefreshToken: ...

    @abstractmethod
    def parse_token(self, token: AccessToken) -> AccessPayload | None: ...
