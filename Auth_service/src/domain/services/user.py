import logging
from os import getenv
from typing import NoReturn

from dotenv import load_dotenv
from starlette.requests import Request

from src.domain.errors import user_error
from src.domain.models import User, UserData, UserID, Role
from src.domain.protocols import (
    UserDAOProtocol,
    SaltProtocol,
    UoWProtocol,
    IdentityProvider,
    RoleProtocol,
)
from src.domain.errors import user_error

load_dotenv()
logging.basicConfig(
    level=logging.WARNING,
    filename=getenv("LOGS_PATH"),
    format="UserService: %(name)s :: %(levelname)s :: %(message)s",
    encoding="utf-8",
    filemode="w",
)


class UserService:
    def __init__(
        self,
        user_repository: UserDAOProtocol,
        salt_repository: SaltProtocol,
        role_repository: RoleProtocol,
        idp: IdentityProvider,
        uow: UoWProtocol,
    ):
        self._user_repository = user_repository
        self._salt_repository = salt_repository
        self._role_repository = role_repository
        self._idp = idp
        self._uow = uow

    async def register_user(self, user_data: UserData) -> UserID:
        user = await self._user_repository.create_user(user_data=user_data)
        await self._uow.commit()
        if user:
            return user

    async def get_user_by_id(self, user_id: UserID) -> User | None:
        return await self._user_repository.get_user_by_id(user_id=user_id)

    async def get_user_by_username(self, username: str) -> User | None:
        return await self._user_repository.get_user_by_username(
            username=username
        )

    async def get_all_users(self) -> list[User]:
        return await self._user_repository.get_all_users()

    async def authenticate_user(
        self, username: str, password: str
    ) -> User | NoReturn:
        user = await self._get_user_all_data_by_username(username=username)
        logging.warning(f"user: {user}, type: {type(user)}")
        try:
            if user and self._validate_password(
                input_password=password, user_password=user.hashed_password
            ):
                return user
        except Exception as e:
            logging.error(f"error: {str(e)}")
        raise ValueError("Bad credentials")

    def _validate_password(
        self, input_password: str, user_password: bytes
    ) -> bool:
        if self._salt_repository.validate_password(
            password=input_password, hashed_password=user_password
        ):
            return True

        return False

    async def _get_user_all_data_by_username(
        self, username: str
    ) -> User | None:
        user = await self._user_repository.get_user_all_data_by_username(
            username=username
        )
        return user

    async def get_current_user(self, request: Request):
        try:
            if not (user_id := self._idp.get_current_user_id(request=request)):
                raise user_error.USER_NOT_EXISTS
            logging.warning(f"user_id: {user_id}, {type(user_id)}")
            return await self._user_repository.get_user_by_id(
                user_id=int(user_id)
            )
        except Exception as e:
            logging.error(f"get_current_user: {str(e)}")

    async def verify_authorized_user(self, request: Request) -> bool:
        role = await self._idp.get_current_user_role(request=request)
        if (role is None) or (not self._role_repository.from_user(role=role)):
            logging.error(
                f"{type(role)} {role} {self._role_repository.from_user(role)}"
            )
            return False
        return True

    async def verify_employee(self, request: Request) -> bool:
        role = await self._idp.get_current_user_role(request=request)
        if (role is None) or (
            not self._role_repository.from_employee(role=role)
        ):
            return False
        return True
