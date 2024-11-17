from src.domain.models import (
    User,
    TokenData,
    TokenTypes,
)
from src.domain.protocols import (
    JWTGenerator,
    JWTStorager,
    UserReaderProtocol,
    UoWProtocol,
)

from salt import SaltService


class AuthService:
    def __init__(
        self,
        jwt_generator: JWTGenerator,
        token_storage: JWTStorager,
        user_reader: UserReaderProtocol,
        uow: UoWProtocol,
        salt: SaltService,
    ):
        self._jwt = jwt_generator
        self._storage = token_storage
        self._reader = user_reader
        self._uow = uow
        self._salt = salt

    def _verify_password(self, user: User, password: str) -> bool:
        return self._salt.validate_password(
            password=password,
            hashed_password=user.hashed_password,
        )

    async def login(self, username: str, password: str) -> TokenData:
        user = await self._reader.get_user_by_username(username)
        if not user or not user.is_active:
            raise Exception("Invalid credentials or user is inactive.")

        if not self._verify_password(user, password):
            raise Exception("Invalid credentials.")

        access_token = self._jwt.create_token(
            user_id=user.id, token_type=TokenTypes.Access
        )
        refresh_token = self._jwt.create_token(
            user_id=user.id, token_type=TokenTypes.Refresh
        )

        await self._storage.save_token(
            user.id, TokenData(access_token, TokenTypes.Access)
        )
        await self._storage.save_token(
            user.id, TokenData(refresh_token, TokenTypes.Refresh)
        )

        return TokenData(token=access_token, token_type=TokenTypes.Access)

    async def refresh(self, refresh_token: str) -> TokenData:
        """
        Refreshing an access token using a refresh token.
        """
        decoded_token = self._jwt.decode_token(
            TokenData(refresh_token, TokenTypes.Refresh)
        )
        user_id = decoded_token.get("sub")

        if not user_id or not self._storage.verify_token(refresh_token):
            raise Exception("Invalid or expired refresh token.")

        user = await self._reader.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise Exception("User not found or inactive.")

        new_access_token = self._jwt.create_token(
            user_id=user.id, token_type=TokenTypes.Access
        )
        await self._storage.save_token(
            user.id, TokenData(new_access_token, TokenTypes.Access)
        )

        return TokenData(token=new_access_token, token_type=TokenTypes.Access)

    async def revoke_refresh_token(self, refresh_token: str) -> None:
        """
        Revoke a specific refresh token.
        """
        if not self._storage.verify_token(refresh_token):
            raise Exception("Invalid or expired refresh token.")

        await self._storage.delete_token(refresh_token)

    async def validate_token(self, token: str, token_type: TokenTypes) -> bool:
        """
        Token validation (access or refresh).
        """
        decoded_token = self._jwt.decode_token(TokenData(token, token_type))
        user_id = decoded_token.get("sub")

        if not user_id or not self._storage.verify_token(token):
            return False

        user = await self._reader.get_user_by_id(user_id)
        return user is not None and user.is_active
