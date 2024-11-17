from src.domain.models import Permissions
from src.domain.protocols import UserReaderProtocol


class PermissionService:
    def __init__(self, user_reader: UserReaderProtocol):
        self._reader = user_reader

    async def has_permission(
        self, user_id: int, permission: Permissions
    ) -> bool:
        user = await self._reader.get_user_by_id(user_id)
        if not user:
            return False
        return user.role.has_permission(permission)
