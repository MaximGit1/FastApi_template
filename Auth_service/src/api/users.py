from dishka.integrations.fastapi import DishkaRoute, FromDishka, inject
from fastapi import APIRouter, HTTPException, Depends, Request
from dotenv import load_dotenv
from os import getenv
import logging

from src.domain.services import UserService, AuthService, CookiesService
from src.domain.models import User, UserID

load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
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
    service: FromDishka[UserService],
) -> User:
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


@inject
async def get_current_user(
        request: Request,
        user_service: FromDishka[UserService],
        auth_service: FromDishka[AuthService],
        cookie_service: FromDishka[CookiesService],
) -> User:
    access_token = cookie_service.get_access_token(request=request)
    user_id = auth_service.get_user_id_by_access_token(
        access_token=access_token
    )
    user = await user_service.get_user_by_id(user_id=user_id)
    return user


@router.get(
    "/me",
    summary="Get current user information",
    response_model_exclude_none=True,
)
async def get_current_user_information(
    user: FromDishka[User],
) -> User:
    return user
