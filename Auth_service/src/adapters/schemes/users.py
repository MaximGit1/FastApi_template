from pydantic import BaseModel, Field

from src.domain.models import User, Roles


class UserInput(BaseModel):
    id: int | None = None
    username: str
    password: bytes
    email: str

    def to_model(self) -> User:
        return User(
            id=self.id if self.id else None,
            username=self.username,
            hashed_password=self.password,
            email=self.email,
        )
