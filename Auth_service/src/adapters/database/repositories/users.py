from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Row, select, update as sa_update
from typing import Sequence, Any

from src.adapters.database.models import users_table
from src.domain.protocols import (
    UserReaderProtocol,
    UserCreatorProtocol,
    SaltProtocol,
    UserUpdaterProtocol,  # for future
)
from src.domain.models import User, Roles
# from .salt import SaltRepository

import logging
from os import getenv
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG, filename=getenv("LOGS_PATH"),
                    format="UserRepository: %(name)s :: %(levelname)s :: %(message)s",
                    encoding="utf-8", filemode="w")


class UserRepository(UserCreatorProtocol, UserReaderProtocol):
    def __init__(
        self, session: AsyncSession, salt: SaltProtocol
    ) -> None:
        self._session = session
        self.__salt = salt

    async def create_user(
        self, username: str, email: str, password: str
    ) -> User:
        role = {
            "value": "user",
            "permissions": Roles.USER,
        }

        user_data = {
            "username": username,
            "email": email,
            "hashed_password": self.__salt.hash_password(password),
            "role": role.get("value"),
            "is_active": True,
            "is_super_user": False,
        }

        stmt = (
            users_table.insert()
            .values(**user_data)
            .returning(users_table.c.id)
        )
        try:
            result = await self._session.execute(stmt)
            new_id = result.scalar_one()

            return User(
                id=new_id,
                username=user_data.get("username"),
                email=user_data.get("email"),
                role=role.get("permissions"),
            )
        except Exception as e:
            logging.exception(f"create_user: {str(e)}")

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(users_table).where(users_table.c.id == user_id)
        result = (await self._session.execute(stmt)).one_or_none()
        return self.__load_user(result) if result else None

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(users_table).where(users_table.c.username == username)
        result = (await self._session.execute(stmt)).one_or_none()
        return self.__load_user(result) if result else None

    async def get_all_users(self) -> list[User]:
        try:
            stmt = select(users_table)
            result = await self._session.execute(stmt)
            return self.__load_users(result.all())
        except Exception as e:
            logging.exception(f"get_all_users: {str(e)}")

    @staticmethod
    def __load_user(row: Row[Any]) -> User:
        try:
            return User(
                id=row.id,
                username=row.username,
                role=row.role,
                is_active=row.is_active,
                is_super_user=row.is_super_user,
            )
        except Exception as e:
            logging.exception(f"__load_user: {str(e)}")

    def __load_users(self, rows: Sequence[Row[Any]]) -> list[User]:
        try:
            return [self.__load_user(row) for row in rows]
        except Exception as e:
            logging.exception(f"__load_users: {str(e)}")

    @staticmethod
    def __get_login_user_data(row: Row[Any]) -> User:
        return User(
            id=row.id,
            username=row.username,
            hashed_password=row.hashed_password,
            role=row.role,
            is_active=row.is_active,
            is_super_user=row.is_super_user,
        )

    async def get_login_user_data_by_username(self, username: str) -> User | None:
        stmt = select(users_table).where(users_table.c.username == username)
        result = (await self._session.execute(stmt)).one_or_none()
        return self.__get_login_user_data(result) if result else None