from datetime import datetime, timedelta
from typing import Any
from jwt import (
    encode,
    decode,
    exceptions as jwt_exceptions,
    ExpiredSignatureError,
    InvalidTokenError,
)
from pathlib import Path
from os import getenv
from dotenv import load_dotenv

from src.domain.protocols import JWTGenerator
from src.domain.models import TokenData, AccessToken, RefreshToken, TokenTypes

load_dotenv()


class JWTRepository(JWTGenerator):
    def __init__(self):
        self.__private_key = self.__load_key(getenv("PRIVATE_KEY_PATH"))
        self.__public_key = self.__load_key(getenv("PUBLIC_KEY_PATH"))
        self.__algorithm = getenv("ALGORITHM", "RS256")
        self.__token_expire_minutes = int(getenv("TOKEN_EXPIRE_MINUTES", 15))
        self.__token_refresh_days = int(getenv("TOKEN_REFRESH_DAYS", 7))

    def create_token(
        self, user_id: int, token_type: AccessToken | RefreshToken
    ) -> TokenData:
        now = datetime.utcnow()
        if token_type is AccessToken:
            expire = now + timedelta(minutes=self.__token_expire_minutes)
            token_type_payload = TokenTypes.Access.value
        elif token_type is RefreshToken:
            expire = now + timedelta(days=self.__token_refresh_days)
            token_type_payload = TokenTypes.Refresh.value
        else:
            raise ValueError(f"Invalid token type: {token_type}")

        payload = {
            "sub": user_id,
            "type": token_type_payload,
            "iat": now,
            "exp": expire,
        }

        token = encode(payload, self.__private_key, algorithm=self.__algorithm)
        return TokenData(
            token=token, token_type=TokenTypes(token_type_payload)
        )

    def decode_token(self, token: TokenData) -> dict:
        try:
            payload = decode(
                token.token,
                self.__public_key,
                algorithms=[self.__algorithm],
                options={"verify_exp": True},
            )
            if payload.get("type") != token.token_type.value:
                raise ValueError("Token type mismatch.")
            return payload
        except ExpiredSignatureError:
            raise ValueError("Token has expired.")
        except InvalidTokenError as e:
            raise ValueError(f"Invalid token: {e}")

    async def validate_token(self, user_id: int, token: TokenData) -> bool:
        try:
            payload = self.decode_token(token)
            return payload.get("sub") == user_id
        except ValueError:
            return False

    @staticmethod
    def __load_key(path: Path | str) -> str:
        base_dir = Path.cwd().parent.parent.parent.parent
        try:
            return Path(base_dir / path).read_text()
        except FileNotFoundError:
            raise RuntimeError(f"Key file not found at path: {path}")
