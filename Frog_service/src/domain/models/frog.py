from dataclasses import dataclass


@dataclass
class Frog:
    id: int | None
    name: str
    age: int
    description: str | None = None
