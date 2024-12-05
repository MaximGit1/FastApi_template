from os import getenv
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(
    level=logging.WARNING,
    filename=getenv("LOGS_PATH"),
    format="RoleRepository: %(name)s :: %(levelname)s :: %(message)s",
    encoding="utf-8",
    filemode="w",
)

from src.domain.models import Role, Roles
from src.domain.protocols import RoleProtocol


class RoleRepository(RoleProtocol):
    def from_user(self, role: Role) -> bool:
        return self._verify_role(
            role=role,
            permission=Roles.User.value,
        )

    def from_employee(self, role: Role) -> bool:
        return self._verify_role(
            role=role,
            permission=Roles.Employee.value,
        )

    def from_admin(self, role: Role) -> bool:
        return self._verify_role(
            role=role,
            permission=Roles.Admin.value,
        )

    @staticmethod
    def _verify_role(role: Role, permission: Role) -> bool:
        if (role.name == permission.name) and (role.level >= permission.level):
            logging.warning(f"role: {role}; permission: {permission}")
            logging.warning(
                f"role.name: {role.name}; permission.name: {permission.name}"
            )
            logging.warning(
                f"role.level: {role.level}; permission.level: {permission.level}"
            )
            logging.warning(
                f"role.name == permission.name is {role.name == permission.name}"
            )
            logging.warning(
                f"role.level >= permission.level is {role.level >= permission.level}"
            )
            return True
        return False

    def is_super_user(self, role: Role) -> bool:
        super_user = Roles.SuperUser.value
        if (role.name == super_user.name) and (role.level == super_user.level):
            return True
        return False
