from dishka.integrations.fastapi import DishkaRoute, FromDishka, inject
from fastapi import APIRouter, HTTPException, Depends, Request
from dotenv import load_dotenv
from os import getenv
import logging

from src.domain.services import UserService, AuthService, CookiesService
from src.domain.models import User, UserID, Role
from src.domain.errors import user_error

load_dotenv()
logging.basicConfig(
    level=logging.WARNING,
    filename=getenv("LOGS_PATH"),
    format="API: %(name)s :: %(levelname)s :: %(message)s",
    encoding="utf-8",
    filemode="w",
)

router = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)


@router.get(
    "/{user_id}/",
    summary="Get the user by id",
    response_model_exclude_none=True,
)
async def get_user_by_id(
    user_id: UserID,
    request: Request,
    service: FromDishka[UserService],
) -> User:
    if not await service.verify_employee(request=request):
        raise user_error.USER_DO_NOT_HAS_THIS_PERMISSION

    user = await service.get_user_by_id(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@router.get(
    "/username/{usermame}/",
    summary="Get the user by username",
    response_model_exclude_none=True,
)
async def get_user_by_username(
    username: str, service: FromDishka[UserService]
) -> User:
    return await service.get_user_by_username(username=username)


@router.get(
    "/",
    summary="Get all users",
    response_model_exclude_none=True,
)
async def get_all_users(service: FromDishka[UserService]) -> list[User]:
    return await service.get_all_users()


@router.get(
    "/me",
    summary="Get current user information",
    response_model_exclude_none=True,
)
async def get_current_user_information(
    request: Request,
    user_service: FromDishka[UserService],
) -> User:
    return await user_service.get_current_user(request=request)


@router.post("/validate-role/")
async def validate_current_user_permission(
    role: Role,
    request: Request,
    service: FromDishka[UserService],
) -> bool:
    user = await service.get_current_user(request=request)
    if not user:
        raise user_error.USER_NOT_EXISTS
    if (user.role.level >= role.level) and (user.role.name == role.name):
        print(user.role, role)
        return True
    return False
