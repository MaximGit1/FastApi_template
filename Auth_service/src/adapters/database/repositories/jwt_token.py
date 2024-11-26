from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
from os import getenv
from jwt import (
    ExpiredSignatureError,
    InvalidTokenError,
    encode,
    decode,
)
import logging
from typing import NoReturn

from src.domain.models import (
    # TokenData,
    AccessToken,
    RefreshToken,
    TokenTypes,
    User,
    Roles,
    AccessPayload,
)
from src.domain.protocols import JWTProtocol


load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    filename=getenv("LOGS_PATH"),
    format="JWTRepository: %(name)s :: %(levelname)s :: %(message)s",
    encoding="utf-8",
    filemode="w",
)


class JWTRepository(JWTProtocol):
    def __init__(self):
        self.__private_key = self._load_key(getenv("PRIVATE_KEY_PATH"))
        self.__public_key = self._load_key(getenv("PUBLIC_KEY_PATH"))
        self.__algorithm = getenv("ALGORITHM", "RS256")
        self.__token_expire_minutes = int(getenv("TOKEN_EXPIRE_MINUTES", 15))
        self.__token_refresh_days = int(getenv("TOKEN_REFRESH_DAYS", 7))

    # def create_token(
    #     self, user: User, token_type: AccessToken | RefreshToken
    # ) -> TokenData:
    #     now = datetime.utcnow()
    #     if token_type is AccessToken:
    #         expire = now + timedelta(minutes=self.__token_expire_minutes)
    #         token_type_payload = TokenTypes.Access.value
    #     elif token_type is RefreshToken:
    #         expire = now + timedelta(days=self.__token_refresh_days)
    #         token_type_payload = TokenTypes.Refresh.value
    #     else:
    #         raise ValueError(f"Invalid token type: {token_type}")
    #     logging.warning(user)
    #     if user.role == "user":
    #         role = Roles.USER
    #     elif user.role == "admin":
    #         role = Roles.ADMIN
    #     else:
    #         role = Roles.GUEST
    #     logging.warning(role)
    #     try:
    #         payload = {
    #             "sub": user.id,
    #             "type": token_type_payload,
    #             "iat": now,
    #             "exp": expire,
    #             "permissions": list(role.value),
    #             "is_active": user.is_active,
    #             "is_super_user": user.is_super_user,
    #         }
    #     except Exception as e:
    #         logging.exception(f"create_token: payload was broken {str(e)}")
    #     try:
    #         token = encode(
    #             payload, self.__private_key, algorithm=self.__algorithm
    #         )
    #         return TokenData(
    #             token=token, token_type=TokenTypes(token_type_payload)
    #         )
    #     except Exception as e:
    #         logging.exception(f"stupid encode: {str(e)}")
    #
    # def decode_token(self, token: TokenData) -> dict:
    #     if not token.token:
    #         raise InvalidTokenError("Invalid token")
    #     try:
    #         payload = decode(
    #             token.token,
    #             self.__public_key,
    #             algorithms=[self.__algorithm],
    #             options={"verify_exp": True},
    #         )
    #         if payload.get("type") != token.token_type.value:
    #             raise ValueError("Token type mismatch.")
    #         return payload
    #     except ExpiredSignatureError:
    #         raise ValueError("Token has expired.")
    #     except InvalidTokenError as e:
    #         raise ValueError("Invalid token")
    #
    # async def validate_token(self, user_id: int, token: TokenData) -> bool:
    #     try:
    #         payload = self.decode_token(token)
    #         return payload.get("sub") == user_id
    #     except ValueError:
    #         return False
    #
    @staticmethod
    def _load_key(path: Path | str) -> str:
        base_dir = Path.cwd().parent.parent.parent.parent
        try:
            return Path(base_dir / path).read_text()
        except FileNotFoundError:
            raise RuntimeError(f"Key file not found at path: {path}")

    #
    # def get_token_payload(self, token: TokenData) -> dict:
    #     payload = self.decode_token(token)
    #     return payload

    def generate_access_token(self, payload: AccessPayload) -> AccessToken:
        token_payload = self._generate_token_payload(
            token_type=TokenTypes.RefreshToken
        )
        payload = {
            "sub": payload.sub,
            "type": token_payload["type"],
            "exp": token_payload["exp"],
        }
        access_token = encode(
            payload, self.__private_key, algorithm=self.__algorithm
        )
        return AccessToken(token=access_token)

    def _generate_token_payload(
        self, token_type: TokenTypes
    ) -> dict | NoReturn:
        now = datetime.utcnow()
        if token_type.value == TokenTypes.AccessToken.value:
            expire = now + timedelta(minutes=self.__token_expire_minutes)
            token_type = TokenTypes.AccessToken.value
        elif token_type.value == TokenTypes.RefreshToken.value:
            expire = now + timedelta(days=self.__token_refresh_days)
            token_type = TokenTypes.RefreshToken.value
        else:
            raise InvalidTokenError("Invalid token")

        return {"exp": expire, "type": token_type}

    def parse_token(self, token: AccessToken) -> AccessPayload | NoReturn:
        payload: AccessPayload = decode(
            token.token,
            self.__public_key,
            algorithms=[self.__algorithm],
            options={"verify_exp": True},
        )
        now = datetime.utcnow()
        if (payload.token_type != token.token_type) or payload.exp < now:
            raise InvalidTokenError("Invalid token")
        return payload
