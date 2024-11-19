from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Row, select, update as sa_update
from typing import Sequence, Any

from src.adapters.database.models import users_table
from src.domain.protocols import UserReaderProtocol, UserCreatorProtocol, UserUpdaterProtocol
from src.domain.models import User


class FrogRepository(UserCreatorProtocol, UserReaderProtocol, UserUpdaterProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

