from typing import ClassVar, Set
from enum import Enum

from .permissions import GlobalPermission

class RolePermission(Enum):
    GUEST: ClassVar[Set[GlobalPermission]] = {
        GlobalPermission.CAN_VIEW_RESOURCE,
        GlobalPermission.CAN_VIEW_RESOURCE_DETAIL,
    }
    USER: ClassVar[Set[GlobalPermission]] = {
        *GUEST,
        GlobalPermission.CAN_CREATE_RESOURCE,
        GlobalPermission.CAN_UPDATE_OWN_RESOURCE,
        GlobalPermission.CAN_DELETE_OWN_RESOURCE,
    }
    ADMIN: ClassVar[Set[GlobalPermission]] = {
        *USER,
        GlobalPermission.CAN_UPDATE_RESOURCE,
        GlobalPermission.CAN_DELETE_RESOURCE,
    }
