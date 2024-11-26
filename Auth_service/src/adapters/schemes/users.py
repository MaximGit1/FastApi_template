from pydantic import BaseModel, EmailStr, Field

from src.domain.models import UserData


class UserLoginInput(BaseModel):
    username: str = Field(min_length=2, max_length=15)
    password: str = Field(min_length=8, max_length=32)

    def to_model(self) -> UserData:
        return UserData(
            username=self.username,
            password=self.password,
            email=None,
        )


class UserRegisterInput(UserLoginInput):
    email: EmailStr = Field(min_length=10, max_length=55)

    def to_model(self) -> UserData:
        user_data = super().to_model()
        user_data.email = self.email
        return user_data
