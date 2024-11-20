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
from .salt import SaltRepository


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

        result = await self._session.execute(stmt)
        new_id = result.scalar_one()

        return User(
            id=new_id,
            username=user_data.get("username"),
            email=user_data.get("email"),
            role=role.get("permissions"),
        )

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(users_table).where(users_table.c.id == user_id)
        result = (await self._session.execute(stmt)).one_or_none()
        return self.__load_user(result) if result else None

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(users_table).where(users_table.c.username == username)
        result = (await self._session.execute(stmt)).one_or_none()
        return self.__load_user(result) if result else None

    async def get_all_users(self) -> list[User]:
        stmt = select(users_table)
        result = await self._session.execute(stmt)
        return self.__load_users(result.all())

    @staticmethod
    def __load_user(row: Row[Any]) -> User:
        return User(
            id=row.id,
            username=row.name,
            role=row.role,
            is_active=row.is_active,
            is_super_user=row.is_super_user,
        )

    def __load_users(self, rows: Sequence[Row[Any]]) -> list[User]:
        return [self.__load_user(row) for row in rows]
