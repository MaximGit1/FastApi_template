from pydantic import BaseModel

from src.domain.models import User, Roles


class UserInput(BaseModel):
    id: int | None = None
    username: str
    password: bytes | str
    email: str

    def to_model(self) -> User:
        return User(
            id=self.id if self.id else None,
            username=self.username,
            hashed_password=self.password,
            email=self.email,
            role=Roles.USER,
        )


class LoginInput(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
