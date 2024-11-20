from src.domain.models import (
    User,
    TokenData,
    TokenTypes,
    AccessToken,
    RefreshToken,
)
from src.domain.protocols import (
    JWTGenerator,
    UserReaderProtocol,
    UoWProtocol,
    UserCreatorProtocol
)

from .salt import SaltService


class AuthService:
    def __init__(
        self,
        jwt_generator: JWTGenerator,
        user_reader: UserReaderProtocol,
        user_saver: UserCreatorProtocol,
        uow: UoWProtocol,
        salt: SaltService,
    ):
        self._jwt = jwt_generator
        self._reader = user_reader
        self._saver = user_saver
        self._uow = uow
        self._salt = salt

    def _verify_password(self, user: User, password: str) -> bool:
        return self._salt.validate_password(
            password=password,
            hashed_password=user.hashed_password,
        )

    async def register(self, username: str, email: str, password: str) -> User:
        # hashed_password = self._salt.hash_password(password)
        user = await self._saver.create_user(username=username, password=password, email=email)
        return user

    async def login(self, username: str, password: str) -> dict:
        """
        Authenticates the user and generates access and refresh tokens.
        """
        user = await self._reader.get_user_by_username(username)
        if not user or not user.is_active:
            raise Exception("Invalid credentials or user is inactive.")

        if not self._verify_password(user, password):
            raise Exception("Invalid credentials.")

        # Generate tokens
        access_token = self._jwt.create_token(
            user_id=user.id, token_type=AccessToken("")
        )
        refresh_token = self._jwt.create_token(
            user_id=user.id, token_type=RefreshToken("")
        )

        return {
            "access_token": access_token.token,
            "refresh_token": refresh_token.token,
        }

    async def logout(self, token_data: TokenData) -> None:
        """
        Validates and "revokes" a token (stateless logout).
        If session-based storage is used, implement token revocation here.
        """
        # If logout is stateless, just validate the token and return.
        try:
            payload = self._jwt.decode_token(token_data)
        except ValueError as e:
            raise Exception(f"Invalid token: {str(e)}")

        # Optionally: check the user_id or other claims in the payload.
        if "sub" not in payload:
            raise Exception("Invalid token payload.")

    async def refresh(self, refresh_token: TokenData) -> dict:
        """
        Generates a new access token using a valid refresh token.
        """
        try:
            payload = self._jwt.decode_token(refresh_token)
            if payload["type"] != TokenTypes.Refresh.value:
                raise Exception("Invalid token type.")
        except ValueError as e:
            raise Exception(f"Invalid refresh token: {str(e)}")

        user_id = payload["sub"]
        new_access_token = self._jwt.create_token(
            user_id=user_id, token_type=AccessToken("")
        )

        return {
            "access_token": new_access_token.token,
        }
