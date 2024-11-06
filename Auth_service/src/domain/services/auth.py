from src.domain.protocols import AuthProtocol, JWT_TOKEN, UowProtocol
from src.domain.models import UserDomain, GlobalPermissionDomain


class AuthService:
    def __init__(
        self, auth_repository: AuthProtocol, uow: UowProtocol
    ) -> None:
        self._auth_repository = auth_repository
        self._uow = uow

    async def register_user(
            self, nickname: str, password: str
    ) -> UserDomain:
        result = await self._auth_repository.register_user(nickname=nickname, password=password)
        await self._uow.commit()
        return result

    async def authenticate_user(
        self, nickname: str, password: str
    ) -> JWT_TOKEN:
        result = await self._auth_repository.authenticate_user(nickname=nickname, password=password)
        await self._uow.commit()
        return result

    async def verify_token(self, token: JWT_TOKEN) -> UserDomain | None:
        result = await self._auth_repository.verify_token(token=token)
        await self._uow.commit()
        return result

    async def check_permission(
        self, user: UserDomain, permission: GlobalPermissionDomain
    ) -> bool:
        result = await self._auth_repository.check_permission(user=user, permission=permission)
        await self._uow.commit()
        return result



