from dotenv import load_dotenv
from typing import Any, NewType
from datetime import timedelta, datetime
from pathlib import Path
from os import getenv
import bcrypt
import jwt

from models import AccessToken, User, RefreshToken


load_dotenv()
BASE_DIR = Path().cwd().parent

Payload = NewType("Payload", dict[str, Any])


class AuthService:
    def __init__(self):
        self.__private_key = self.__load_key(
            BASE_DIR / getenv("PRIVATE_KEY_PATH")
        )
        self.__public_key = self.__load_key(
            BASE_DIR / getenv("PUBLIC_KEY_PATH")
        )
        self.__algorithm = getenv("ALGORITHM")
        self.__token_expire = int(getenv("TOKEN_EXPIRE_MINUTES"))
        self.__token_refresh = int(getenv("TOKEN_REFRESH_DAYS"))

    @staticmethod
    def __load_key(key_path: Path):
        return Path(key_path).read_text()

    def encode(
        self, payload: Payload, expire_timedelta: timedelta | None = None
    ) -> AccessToken:
        now = datetime.utcnow()
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            if payload.get("type") == "access":
                expire = now + timedelta(minutes=self.__token_expire)
            elif payload.get("type") == "refresh":
                expire = now + timedelta(days=self.__token_refresh)
            else:
                raise TypeError("Invalid token type")

        payload["exp"] = expire
        payload["iat"] = now
        print(f"iat:{now}, exp:{expire}")

        token: AccessToken = jwt.encode(
            payload=payload,
            key=self.__private_key,
            algorithm=self.__algorithm,
        )
        return token

    def decode(self, token: AccessToken) -> Payload:
        decoded: Payload = jwt.decode(
            jwt=token,
            key=self.__public_key,
            algorithms=[self.__algorithm],
        )
        return decoded

    def __create_token(self, payload: Payload) -> AccessToken | RefreshToken:
        return self.encode(payload)

    def create_access_token(self, user: User) -> AccessToken:
        payload: Payload = {"sub": user.username, "type": "access"}  # sub=id
        return self.__create_token(payload)

    def create_refresh_token(self, user: User) -> RefreshToken:
        payload: Payload = {"sub": user.username, "type": "refresh"}  # sub=id
        return self.__create_token(payload)


class Salt:
    @staticmethod
    def hash_password(password: str) -> bytes:
        return bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())

    @staticmethod
    def validate_password(password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )


auth_service = AuthService()
