from typing import ClassVar, Set
from enum import Enum

from permissions import Permissions


class Roles(Enum):
    GUEST: ClassVar[Set[Permissions]] = {
        Permissions.CAN_VIEW_RESOURCE,
        Permissions.CAN_VIEW_RESOURCE_DETAIL,
    }
    USER: ClassVar[Set[Permissions]] = {
        *GUEST,
        Permissions.CAN_CREATE_RESOURCE,
        Permissions.CAN_UPDATE_OWN_RESOURCE,
        Permissions.CAN_DELETE_OWN_RESOURCE,
    }
    ADMIN: ClassVar[Set[Permissions]] = {
        *USER,
        Permissions.CAN_UPDATE_RESOURCE,
        Permissions.CAN_DELETE_RESOURCE,
    }
