from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.dml import ReturningInsert
from sqlalchemy import Row, select
from typing import Sequence, Any
from dotenv import load_dotenv
from typing import NoReturn
from os import getenv
import logging


from src.domain.errors import user_error
from src.adapters.database.models import users_table
from src.domain.models import User, Roles, UserID, UserData
from src.domain.protocols import UserDAOProtocol, SaltProtocol


load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    filename=getenv("LOGS_PATH"),
    format="UserRepository: %(name)s :: %(levelname)s :: %(message)s",
    encoding="utf-8",
    filemode="w",
)


class UserRepository(UserDAOProtocol):
    def __init__(self, session: AsyncSession, salt: SaltProtocol) -> None:
        self._session = session
        self.__salt = salt
        self._base_user_role = Roles.User.name

    async def create_user(self, user_data: UserData) -> UserID | NoReturn:
        user_data_payload = self._generate_user_data_payload(
            user_data=user_data
        )

        stmt = (
            users_table.insert()
            .values(**user_data_payload)
            .returning(users_table.c.id)
        )

        if user_id := await self._try_to_add_user(stmt=stmt):
            return user_id
        raise user_error.USER_ALREADY_EXISTS

    async def _try_to_add_user(
        self, stmt: ReturningInsert[tuple[Any]]
    ) -> UserID | NoReturn:
        try:
            result = await self._session.execute(stmt)
            new_id = result.scalar_one()

            return new_id
        except Exception as e:
            logging.exception(e)

    def _generate_user_data_payload(self, user_data: UserData) -> dict:
        return {
            "username": user_data.username,
            "email": user_data.email,
            "hashed_password": self.__salt.hash_password(user_data.password),
            "role": self._base_user_role,
            "is_active": True,
        }

    async def get_user_by_id(self, user_id: UserID) -> User | None:
        stmt = select(users_table).where(users_table.c.id == user_id)
        result = (await self._session.execute(stmt)).one_or_none()
        return self._load_user(result) if result else None

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(users_table).where(users_table.c.username == username)
        result = (await self._session.execute(stmt)).one_or_none()
        return self._load_user(result) if result else None

    async def get_all_users(self) -> list[User]:
        stmt = select(users_table)
        result = await self._session.execute(stmt)
        return self._load_users(rows=result.all())

    @staticmethod
    def _load_user(row: Row[Any]) -> User:
        return User(
            id=row.id,
            username=row.username,
            email=row.email,
            role=Roles.get_role_by_name(name=row.role),
            is_active=row.is_active,
        )

    def _load_users(self, rows: Sequence[Row[Any]]) -> list[User]:
        return [self._load_user(row) for row in rows]

    async def get_user_all_data_by_username(
        self, username: str
    ) -> User | None:
        stmt = select(users_table).where(users_table.c.username == username)
        result = (await self._session.execute(stmt)).one_or_none()
        return self._load_user_with_password(result) if result else None

    @staticmethod
    def _load_user_with_password(row: Row[Any]) -> User:
        return User(
            id=row.id,
            username=row.username,
            email=row.email,
            role=Roles.get_role_by_name(name=row.role),
            is_active=row.is_active,
            hashed_password=row.hashed_password,
        )
