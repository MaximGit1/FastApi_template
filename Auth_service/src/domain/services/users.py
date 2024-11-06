from src.domain.models import UserDomain
from src.domain.protocols import UserProtocol, UowProtocol


class FrogService:
    def __init__(
        self, user_repository: UserProtocol, uow: UowProtocol
    ) -> None:
        self._user_repository = user_repository
        self._uow = uow

    async def get_all(self) -> list[UserDomain]:
        return await self._user_repository.get_all()

    async def get_by_id(self, user_id: int) -> UserDomain | None:
        return await self._user_repository.get_by_id(user_id=user_id)

    async def create(self, user: UserDomain) -> UserDomain:
        result = await self._user_repository.create(user=user)
        await self._uow.commit()
        return result

    async def update(self, user: UserDomain) -> bool:
        try:
            await self._user_repository.update(user=user)
            await self._uow.commit()
        except Exception as exc:
            await self._uow.rollback()
            return False

        return True

    async def delete_by_id(self, user_id: int) -> None:
        await self._user_repository.delete_by_id(user_id=user_id)
        await self._uow.commit()