from dataclasses import dataclass
from typing import NewType
from enum import Enum

RoleLevel = NewType("RoleLevel", int)


@dataclass
class Role:
    name: str
    level: RoleLevel


class Roles(Enum):
    Guest = Role(name="guest", level=RoleLevel(0))
    User = Role(name="user", level=RoleLevel(1))
    Employer = Role(name="employer", level=RoleLevel(2))
    Admin = Role(name="admin", level=RoleLevel(3))
    SuperUser = Role(name="superUser", level=RoleLevel(4))

    @classmethod
    def get_role_by_name(cls, name: str) -> Role:
        roles = cls._member_map_
        for role in (role for role in roles):
            if name.lower() == role.lower():
                print(name, role)
                return roles[role].value

        return cls.Guest.value
