from starlette.requests import Request
from dotenv import load_dotenv
from os import getenv
import logging

from src.domain.protocols import (
    IdentityProvider,
    UserDAOProtocol,
    CookieProtocol,
    JWTProtocol,
)
from src.domain.models import UserID, Role, AccessToken, Token

load_dotenv()

logging.basicConfig(
    level=logging.WARNING,
    filename=getenv("LOGS_PATH"),
    format="IDPRepository: %(name)s :: %(levelname)s :: %(message)s",
    encoding="utf-8",
    filemode="w",
)


class JWTIdentityProvider(IdentityProvider):
    def __init__(
        self,
        cookie_repository: CookieProtocol,
        jwt_repository: JWTProtocol,
        user_repository: UserDAOProtocol,
    ):
        self._user_id: UserID | None = None
        self._cookie_repository = cookie_repository
        self._jwt_repository = jwt_repository
        self._user_repository = user_repository
        self._auth_access_token = getenv("AUTH_ACCESS_TOKEN")

    def get_current_user_id(self, request: Request) -> UserID | None:
        try:
            if not self._has_user_id():
                token: Token | str = self._cookie_repository.get_cookie_value(
                    request=request, key=self._auth_access_token
                )
                access_token = AccessToken(token=token)
                sub = (
                    self._jwt_repository.parse_token(token=access_token)
                ).sub
                logging.warning(f"sub={sub}")
                self._user_id = int(sub)
                return UserID(sub)

            return UserID(self._user_id)
        except Exception as e:
            logging.error(f"get_current_user_id {e}")

    def _has_user_id(self) -> bool:
        if self._user_id is None:
            return False
        return True

    async def get_current_user_role(self, request: Request) -> Role | None:
        if not self._has_user_id():
            user_id = self.get_current_user_id(request=request)
            user = await self._user_repository.get_user_by_id(
                user_id=int(user_id)
            )
        else:
            user = await self._user_repository.get_user_by_id(
                user_id=self._user_id
            )

        if user.is_active:
            return user.role

        return None
