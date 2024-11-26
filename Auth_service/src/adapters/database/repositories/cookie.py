from urllib.request import Request

from dotenv import load_dotenv
from os import getenv
from starlette.responses import Response
from datetime import datetime, timedelta

from src.domain.protocols import CookieProtocol


load_dotenv()


class CookieRepository(CookieProtocol):
    def __init__(self):
        self._cookie_max_age_days = self._load_cookie_max_age(
            key=getenv("COOKIE_MAX_AGE_DAYS")
        )

    def set_cookie_value(
        self, response: Response, key: str, value: str
    ) -> None:
        response.set_cookie(
            key=key,
            value=value,
            httponly=True,
            max_age=self._cookie_max_age_days,
        )

    def get_cookie_value(self, response: Response, key: str) -> str | None:
        pass

    def delete_cookie(self, response: Response, key: str) -> None:
        response.delete_cookie(key=key)

    def _load_cookie_max_age(self, key: str) -> int:
        days = int(key)
        return days * 24 * 60 * 60
