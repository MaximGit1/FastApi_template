from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, status, Depends
from dotenv import load_dotenv
from os import getenv
import logging

from src.domain.services import UserService
from src.adapters.schemes import UserLoginInput, UserRegisterInput
from src.domain.models import User, UserID, UserData

load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    filename=getenv("LOGS_PATH"),
    format="API: %(name)s :: %(levelname)s :: %(message)s",
    encoding="utf-8",
    filemode="w",
)

router = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)


# @router.get("/", summary="Get all users", response_model_exclude_none=True)
# async def get_all(service: FromDishka[UserService]) -> list[User]:
#     try:
#         results: list[User] = await service.get_all_users()
#         return results
#     except Exception as e:
#         logging.exception(f"get_all: {str(e)}")


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


@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    user_input: UserRegisterInput, service: FromDishka[UserService]
) -> UserID:
    user_id = await service.register_user(user_data=user_input.to_model())
    return user_id
