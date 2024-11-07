from sqlalchemy import (
    Table,
    MetaData,
    Column,
    TIMESTAMP,
    Boolean,
    String,
    Integer,
    func,
)
from sqlalchemy.orm import registry

from src.domain.models import UserDomain


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
    Column("nickname", String(15), nullable=False),
    Column("password", String(30), nullable=False),
    Column("role", String(5), nullable=False, default="GUEST", server_default="GUEST"),
    Column("is_super_user", Boolean, default=True),
    Column("is_active", Boolean, default=True),
    Column(
        "created_at",
        TIMESTAMP,
        default=func.now(),
        server_default=func.now(),
        nullable=False,
    ),
    Column(
        "updated_at",
        TIMESTAMP,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        server_onupdate=func.now(),
        nullable=True,
    ),
)


def map_tables() -> None:
    mapper_registry.map_imperatively(UserDomain, users_table)