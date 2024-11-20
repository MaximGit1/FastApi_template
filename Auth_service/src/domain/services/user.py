from src.domain.models import User, Roles
from src.domain.protocols import (
    UserReaderProtocol,
    UserCreatorProtocol,
    UserUpdaterProtocol,
    UoWProtocol,
)

import logging
from os import getenv
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG, filename=getenv("LOGS_PATH"),
                    format="UserService: %(name)s :: %(levelname)s :: %(message)s\n\n\n",
                    encoding="utf-8", filemode="w")


class UserService:
    def __init__(
        self,
        user_reader: UserReaderProtocol,
        user_creator: UserCreatorProtocol,
        # user_updater: UserUpdaterProtocol,
        uow: UoWProtocol,
    ):
        self._reader = user_reader
        self._creator = user_creator
        # self._updater = user_updater
        self._uow = uow

    async def get_user_by_id(self, user_id: int) -> User | None:
        try:
            return await self._reader.get_user_by_id(user_id)
        except Exception as e:
            logging.exception(f"get_user_by_id: {str(e)}")

    async def get_user_by_username(self, username: str) -> User | None:
        return await self._reader.get_user_by_username(username=username)

    async def get_login_user_data_by_username(self, username: str) -> User | None:
        return await self._reader.get_login_user_data_by_username(username=username)

    async def create_user(
        self, username: str, email: str, password: str
    ) -> User:
        try:
            async with self._uow:
                user = await self._creator.create_user(username, email, password)
                await self._uow.commit()
                return user
        except Exception as e:
            logging.exception(f"create_user: {str(e)}")



    async def get_all_users(self):
        async with self._uow:
            user = await self._reader.get_all_users()
            await self._uow.commit()
            return user

    # async def update_user_role(self, user_id: int, role: Roles) -> bool:
    #     async with self._uow:
    #         result = await self._updater.update_user_role(user_id, role)
    #         await self._uow.commit()
    #         return result
    #
    # async def deactivate_user(self, user_id: int) -> None:
    #     async with self._uow:
    #         await self._updater.deactivate_user(user_id)
    #         await self._uow.commit()
    #
    # async def activate_user(self, user_id: int) -> None:
    #     async with self._uow:
    #         await self._updater.activate_user(user_id)
    #         await self._uow.commit()
