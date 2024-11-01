from pydantic import BaseModel, Field

from src.domain.models import FrogDomain


class Frog(BaseModel):
    id: int
    name: str = Field(max_length=15)
    age: int
    description: str | None = Field(max_length=200)

    def to_model(self) -> FrogDomain:
        return FrogDomain(
            id=self.id,
            name=self.name,
            description=self.description,
            age=self.age,
        )
