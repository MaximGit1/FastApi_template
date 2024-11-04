from typing import Type
from enum import Enum


class PermissionHelper:
    auto_value = 0

    @classmethod
    def auto(cls):
        cls.auto_value += 1
        return cls.auto_value

    @staticmethod
    def generate_permission_enum(*enum_permissions: Type[Enum]) -> Enum:
        all_permissions = {}

        for permissions in enum_permissions:
            for permission in permissions:
                all_permissions[permission.name] = permission.value

        return Enum("Permissions", all_permissions)


auto = lambda: PermissionHelper.auto()


class FrogPermission(Enum):
    CAN_VIEW_FROG = auto()
    CAN_CREATE_FROG = auto()
    CAN_UPDATE_FROG = auto()
    CAN_DELETE_FROG = auto()


class UserPermission(Enum):
    CAN_VIEW_USERS = auto()
    CAN_DELETE_USER = auto()
    CAN_UPDATE_USER_ROLE = auto()


Permission = PermissionHelper.generate_permission_enum(
    FrogPermission,
    UserPermission,
)
