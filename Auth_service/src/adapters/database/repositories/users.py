from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Row, select, update as sa_update
from typing import Sequence, Any

from src.adapters.database.models import users_table
from src.domain.protocols import UserProtocol
from src.domain.models import UserDomain, RolePermissionDomain


class UserRepository(UserProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _set_user_role(role_name: str) -> RolePermissionDomain:
        if role_name == "USER":
            role = RolePermissionDomain.USER
        elif role_name == "Admin":
            role = RolePermissionDomain.ADMIN
        else:
            role = RolePermissionDomain.GUEST
        return role

    def _load_user(self, row: Row[Any]) -> UserDomain:
        return UserDomain(
            id=row.id,
            nickname=row.nickname,
            # password=row.password,
            role=self._set_user_role(row.role),
            is_active=row.is_active,
            is_super_user=row.is_super_user,
        )

    def _load_users(self, rows: Sequence[Row[Any]]) -> list[UserDomain]:
        return [self._load_user(row) for row in rows]

    async def get_all(self) -> list[UserDomain]:
        stmt = select(users_table)
        result = await self._session.execute(stmt)
        return self._load_users(result.all())

    async def get_by_id(self, user_id: int) -> UserDomain | None:
        stmt = select(users_table).where(users_table.c.id == user_id)
        result = (await self._session.execute(stmt)).one_or_none()
        return self._load_user(result) if result else None

    async def create(self, user: UserDomain) -> UserDomain:
        user_values = {
            "nickname": user.nickname,
            "role": user.role,
            "password": user.password,  # hashed_pass
            "is_active": True,
            "is_super_user": False,
        }

        if user.id:
            user_values["id"] = user.id

        stmt = (
            users_table.insert()
            .values(**user_values)
            .returning(users_table.c.id)
        )

        result = await self._session.execute(stmt)
        new_id = result.scalar_one()

        return UserDomain(
            id=new_id,
            nickname=user.nickname,
            role=self._set_user_role(user_values["role"]),
            is_active=user.is_active,
            is_super_user=user.is_super_user,
        )

    async def update(self, user: UserDomain) -> bool:
        stmt = (
            sa_update(users_table)
            .where(users_table.c.id == user.id)
            .values(nickname=user.nickname)
        )
        result = await self._session.execute(stmt)

        if result.rowcount > 0:
            return True

        return False

    async def delete_by_id(self, user_id: int) -> None:
        stmt = users_table.delete().where(users_table.c.id == user_id)
        await self._session.execute(stmt)
