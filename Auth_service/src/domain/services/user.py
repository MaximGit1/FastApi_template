from src.domain.models import User, Roles
from src.domain.protocols import UserReaderProtocol, UserCreatorProtocol, UserUpdaterProtocol, UoWProtocol

class UserService:
    def __init__(
        self,
        user_reader: UserReaderProtocol,
        user_creator: UserCreatorProtocol,
        user_updater: UserUpdaterProtocol,
        uow: UoWProtocol,
    ):
        self._reader = user_reader
        self._creator = user_creator
        self._updater = user_updater
        self._uow = uow

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self._reader.get_user_by_id(user_id)

    async def register_user(self, username: str, email: str, password: str) -> User:
        async with self._uow:
            user = await self._creator.create_user(username, email, password)
            await self._uow.commit()
            return user

    async def update_user_role(self, user_id: int, role: Roles) -> bool:
        async with self._uow:
            result = await self._updater.update_user_role(user_id, role)
            await self._uow.commit()
            return result

    async def deactivate_user(self, user_id: int) -> None:
        async with self._uow:
            await self._updater.deactivate_user(user_id)
            await self._uow.commit()

    async def activate_user(self, user_id: int) -> None:
        async with self._uow:
            await self._updater.activate_user(user_id)
            await self._uow.commit()
