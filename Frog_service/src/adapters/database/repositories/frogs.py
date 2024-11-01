from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Row, select
from typing import Sequence, Any

from src.adapters.database.models import frogs_table
from src.domain.protocols import FrogProtocol
from src.domain.models import FrogDomain


class FrogRepository(FrogProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _load_frog(row: Row[Any]) -> FrogDomain:
        return FrogDomain(id=row.id, name=row.name, age=row.age, description=row.description)

    def _load_frogs(self, rows: Sequence[Row[Any]]) -> list[FrogDomain]:
        return [self._load_frog(row) for row in rows]

    async def get_all(self) -> list[FrogDomain]:
        stmt = select(frogs_table)
        result = await self._session.execute(stmt)
        return self._load_frogs(result.all())

    async def get_by_id(self, frog_id: int) -> FrogDomain | None:
        stmt = select(frogs_table).where(frogs_table.c.id == frog_id)
        result = (await self._session.execute(stmt)).one_or_none()
        return self._load_frog(result) if result else None

    async def create(self, frog: FrogDomain) -> FrogDomain:
        stmt = frogs_table.insert().values(
            id=frog.id,
            name=frog.name,
            age=frog.age,
            description=frog.description
        ).returning(frogs_table.c.id)

        result = await self._session.execute(stmt)
        new_id = result.scalar_one()

        return FrogDomain(
            id=new_id,
            name=frog.name,
            age=frog.age,
            description=frog.description
        )

    async def update(self, frog: FrogDomain) -> bool:
        return False

    async def delete_by_id(self, frog_id: int) -> None:
        stmt = frogs_table.delete().where(frogs_table.c.id==frog_id)
        await self._session.execute(stmt)

