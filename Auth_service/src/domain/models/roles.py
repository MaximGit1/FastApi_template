from enum import Enum
from typing import ClassVar, Set

from permissions import Permission


class RolePermission(Enum):
    GUEST: ClassVar[Set[Permission]] = {
        Permission.CAN_VIEW_FROG,
    }
    DEFAULT: ClassVar[Set[Permission]] = {
        *GUEST,
        Permission.CAN_CREATE_FROG,
        Permission.CAN_UPDATE_FROG,
        Permission.CAN_DELETE_FROG,
    }
    ADMIN: ClassVar[Set[Permission]] = {
        *DEFAULT,
        Permission.CAN_VIEW_USERS,
        Permission.CAN_DELETE_USER,
        Permission.CAN_UPDATE_USER_ROLE,
    }
