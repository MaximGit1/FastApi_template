import logging
from datetime import datetime, timedelta
from os import getenv
from dotenv import load_dotenv

from src.domain.models import User, AccessToken, UserID, AccessPayload
from src.domain.protocols import JWTProtocol

load_dotenv()
logging.basicConfig(
    level=logging.WARNING,
    filename=getenv("LOGS_PATH"),
    format="AuthService: %(name)s :: %(levelname)s :: %(message)s",
    encoding="utf-8",
    filemode="w",
)


class AuthService:
    def __init__(self, jwt_generator: JWTProtocol):
        self._repository_generator = jwt_generator

    def login_user(self, user: User) -> AccessToken:
        payload = self._create_user_data_payload(user=user)
        access_token = self._generate_access_token(payload=payload)
        return access_token

    def get_user_id_by_access_token(
        self, access_token: AccessToken
    ) -> UserID | None:
        try:
            payload = self._parse_access_token(access_token=access_token)
            payload = AccessPayload(
                sub=UserID(int(payload.sub)),
                exp=payload.exp,
                token_type=payload.token_type,
            )
            logging.warning(f"get_user_id_by_access_token: payload: {payload}")
            if self._validate_token_expire(payload=payload):
                logging.warning(
                    f"get_user_id_by_access_token: _validate_token_expire: {self._validate_token_expire(payload=payload)}"
                )
                logging.warning(
                    f"get_user_id_by_access_token: {payload.sub}, {type(payload.sub)}"
                )
                return payload.sub
            return None
        except Exception as e:
            logging.error(f"get_user_id_by_access_token: {str(e)}")

    @staticmethod
    def _validate_token_expire(payload: AccessPayload) -> bool:
        try:
            expire: int = payload.exp
            now = datetime.utcnow().timestamp()
            if expire and (expire > now):
                return True
            return False
        except Exception as e:
            logging.error(f"_validate_token_expire: {str(e)}")

    def _parse_access_token(
        self, access_token: AccessToken
    ) -> AccessPayload | None:
        try:
            return self._repository_generator.parse_token(token=access_token)
        except Exception as e:
            logging.error(f"_parse_access_token: {str(e)}!!!!")
            raise e

    def _generate_access_token(self, payload: AccessPayload) -> AccessToken:
        """
        Получает payload с данными пользователя и дополняет данными access токена.
        """
        access_token = self._repository_generator.generate_access_token(
            payload=payload,
        )
        return access_token

    @staticmethod
    def _create_user_data_payload(user: User) -> AccessPayload:
        """
        Получает пользователя и подготавливает данные пользователя для генерации jwt access token
        """
        payload = AccessPayload(
            sub=user.id,
        )
        return payload
