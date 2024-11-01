from pydantic import BaseModel, Field

from src.domain.models import FrogDomain


class Frog(BaseModel):
    id: int | None = None
    name: str = Field(max_length=15)
    age: int
    description: str | None = Field(max_length=200)

    def to_model(self) -> FrogDomain:
        return FrogDomain(
            id=self.id if self.id else None,
            name=self.name,
            description=self.description,
            age=self.age,
        )
