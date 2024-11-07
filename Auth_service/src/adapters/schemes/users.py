from pydantic import BaseModel, Field

from src.domain.models import UserDomain
from src.domain.models.roles import RolePermission


class UserScheme(BaseModel):
    id: int | None = None
    nickname: str = Field(max_length=15)
    password: bytes | str
    role: str
    is_super_user: bool = False
    is_active: bool = True

    def to_model(self) -> UserDomain:
        return UserDomain(
            id=self.id if self.id else None,
            nickname=self.nickname,
            password=self.password,
            role=self.role,
            is_super_user=True if self.is_super_user else False,
            is_active=True if self.is_active else False,
        )