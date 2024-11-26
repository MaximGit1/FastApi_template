from sqlalchemy import (
    LargeBinary,
    TIMESTAMP,
    MetaData,
    Integer,
    Boolean,
    Column,
    String,
    Table,
    func,
)
from sqlalchemy.orm import registry

from src.domain.models import User


metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)
mapper_registry = registry(metadata=metadata)


users_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(25), nullable=False, unique=True),
    Column("email", String(55), nullable=False),
    Column("hashed_password", LargeBinary, nullable=False),
    Column("role", String(10), nullable=False),
    Column("is_active", Boolean, nullable=False, default=True),
    Column(
        "created_at",
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    ),
    Column(
        "updated_at",
        TIMESTAMP,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    ),
)


def map_tables() -> None:
    mapper_registry.map_imperatively(User, users_table)
