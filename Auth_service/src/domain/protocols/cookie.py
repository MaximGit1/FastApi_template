from abc import abstractmethod
from typing import Protocol

from starlette.responses import Response
from starlette.requests import Request


class CookieProtocol(Protocol):
    @abstractmethod
    def get_cookie_value(self, request: Request, key: str) -> str | None: ...

    @abstractmethod
    def set_cookie_value(
        self, response: Response, key: str, value: str
    ) -> None: ...

    @abstractmethod
    def delete_cookie(self, response: Response, key: str) -> None: ...
