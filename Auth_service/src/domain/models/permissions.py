from enum import Enum


class Permissions(str, Enum):
    CAN_VIEW_OWN_RESOURCE = "can_view_own_resource"
    CAN_UPDATE_OWN_RESOURCE = "can_update_own_resource"
    CAN_DELETE_OWN_RESOURCE = "can_delete_own_resource"

    CAN_VIEW_RESOURCE = "can_view_resource"
    CAN_VIEW_RESOURCE_DETAIL = "can_view_resource_detail"
    CAN_CREATE_RESOURCE = "can_create_resource"
    CAN_UPDATE_RESOURCE = "can_update_resource"
    CAN_DELETE_RESOURCE = "can_delete_resource"
