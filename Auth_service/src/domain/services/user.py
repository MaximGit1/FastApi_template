import logging
from os import getenv
from dotenv import load_dotenv

from src.domain.models import User
from src.domain.protocols import (
    UserReaderProtocol,
    UserCreatorProtocol,
    UoWProtocol,
)


load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    filename=getenv("LOGS_PATH"),
    format="UserService: %(name)s :: %(levelname)s :: %(message)s",
    encoding="utf-8",
    filemode="w",
)


class UserService:
    def __init__(
        self,
        user_reader: UserReaderProtocol,
        user_creator: UserCreatorProtocol,
        uow: UoWProtocol,
    ):
        self._reader = user_reader
        self._creator = user_creator
        self._uow = uow

    async def get_user_by_id(self, user_id: int) -> User | None:
        try:
            return await self._reader.get_user_by_id(user_id)
        except Exception as e:
            logging.exception(f"get_user_by_id: {str(e)}")

    async def get_user_by_username(self, username: str) -> User | None:
        return await self._reader.get_user_by_username(username=username)

    async def get_login_user_data_by_username(
        self, username: str
    ) -> User | None:
        return await self._reader.get_login_user_data_by_username(
            username=username
        )

    async def create_user(
        self, username: str, email: str, password: str
    ) -> User:
        try:
            async with self._uow:
                user = await self._creator.create_user(
                    username, email, password
                )
                await self._uow.commit()
                return user
        except Exception as e:
            logging.exception(f"create_user: {str(e)}")

    async def get_all_users(self):
        async with self._uow:
            user = await self._reader.get_all_users()
            await self._uow.commit()
            return user
