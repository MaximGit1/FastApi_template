from urllib.request import Request

from starlette.responses import Response
from dotenv import load_dotenv
from os import getenv

from src.domain.protocols import CookieProtocol
from src.domain.models import AccessToken, Token


load_dotenv()


class CookiesService:
    def __init__(self, cookies_repository: CookieProtocol):
        self._cookies_repository = cookies_repository
        self._auth_access_token = getenv("AUTH_ACCESS_TOKEN")

    def get_access_token(self, request: Request) -> AccessToken | None:
        access_token_value: Token | str = (
            self._cookies_repository.get_cookie_value(
                request=request,
                key=self._auth_access_token,
            )
        )
        if access_token_value:
            return AccessToken(token=access_token_value)

        return None

    def set_set_access_token(self, value: str, response: Response) -> None:
        self._cookies_repository.set_cookie_value(
            response=response,
            key=self._auth_access_token,
            value=value,
        )

    def delete_access_token(self, response: Response) -> None:
        self._cookies_repository.delete_cookie(
            response=response, key=self._auth_access_token
        )
