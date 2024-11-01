from src.domain.models import FrogDomain
from src.domain.protocols import FrogProtocol, UowProtocol


class FrogService:
    def __init__(
        self, frog_repository: FrogProtocol, uow: UowProtocol
    ) -> None:
        self._frog_repository = frog_repository
        self._uow = uow

    async def get_all(self) -> list[FrogDomain]:
        return await self._frog_repository.get_all()

    async def get_by_id(self, frog_id: int) -> FrogDomain | None:
        return await self._frog_repository.get_by_id(frog_id=frog_id)

    async def create(self, frog: FrogDomain) -> FrogDomain:
        result = await self._frog_repository.create(frog=frog)
        await self._uow.commit()
        return result

    async def update(self, frog: FrogDomain) -> bool:
        try:
            await self._frog_repository.update(frog=frog)
            await self._uow.commit()
        except Exception as exc:
            await self._uow.rollback()
            return False

        return True

    async def delete_by_id(self, frog_id: int) -> None:
        await self._frog_repository.delete_by_id(frog_id=frog_id)
        await self._uow.commit()
