from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Row, select, update as sa_update
from typing import Sequence, Any, Protocol
from dotenv import load_dotenv
from pathlib import Path
import jwt
import os

from src.adapters.database.models import users_table
from src.domain.protocols import AuthProtocol, JWT_TOKEN
from src.domain.models import UserDomain, RolePermissionDomain
from .salt import SaltService


load_dotenv()
BASE_DIR = Path.cwd().parent.parent.parent.parent


class AuthRepository(Protocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.__private_key = self.__load_key(
            BASE_DIR / os.getenv("PRIVATE_KEY_PATH")
        )
        self.__public_key = self.__load_key(
            BASE_DIR / os.getenv("PUBLIC_KEY_PATH")
        )
        self.__algorithm = os.getenv("ALGORITHM")
        self.__salt = SaltService()
        self.__token_expire_minutes = os.getenv("TOKEN_EXPIRE_MINUTES")

    @staticmethod
    def __load_key(jwt_key_path: Path) -> str:
        with open(jwt_key_path, "r") as file:
            key = file.read()
        return key

    def __encode(self, payload: dict):
        return jwt.encode(
            payload=payload,
            key=self.__private_key,
            algorithm=self.__algorithm,
        )

    def __decode(self, token: str | bytes):
        return jwt.decode(
            jwt=token,
            key=self.__public_key,
            algorithms=self.__algorithm,
        )

    async def authenticate_user(
        self, nickname: str, password: str, sub: int
    ) -> JWT_TOKEN:
        payload = {
            "nickname": nickname,
            "password": password,
            "sub": sub,
            "exp": self.__token_expire_minutes,
        }
        access_token = self.__encode(payload)
        return access_token
