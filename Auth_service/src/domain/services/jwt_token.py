from typing import Type

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
from src.domain.models import TokenResponse

import logging
from os import getenv
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG, filename=getenv("LOGS_PATH"),
                    format="AuthServicePythoooon: %(name)s :: %(levelname)s :: %(message)s",
                    encoding="utf-8", filemode="w")

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
        try:
            user = await self._saver.create_user(username=username, password=password, email=email)
            return user
        except Exception as e:
            logging.exception(f"register: {str(e)}")

    async def login(self, username: str, password: str) -> TokenResponse:
        """
        Authenticates the user and generates access and refresh tokens.
        """
        try:
            user: User = await self._reader.get_login_user_data_by_username(username)
            if not user or not user.is_active:
                raise Exception("Invalid credentials or user is inactive.")
        except Exception as e:
            logging.exception(f"login, user not exist: {str(e)}")

        try:
            if not self._verify_password(user, password):
                raise Exception("Invalid credentials.")
        except Exception as e:
            logging.exception(f"login, password do not validate: {str(e)}")

        try: # тут ошибка
            access_token = self._jwt.create_token(
                user_id=user.id, token_type=AccessToken
            )
            refresh_token = self._jwt.create_token(
                user_id=user.id, token_type=RefreshToken
            )

            return TokenResponse(
                access_token=access_token.token,
                refresh_token=refresh_token.token,
            )
        except Exception as e:
            logging.exception(f"login, token do not generated: {str(e)}")



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

