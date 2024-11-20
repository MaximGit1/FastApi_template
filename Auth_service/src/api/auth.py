from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, status
import logging
from os import getenv
from dotenv import load_dotenv

from src.domain.models import TokenData, User, TokenResponse
from src.domain.services import UserService, AuthService
from src.adapters.schemes import UserInput, LoginInput

load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    filename=getenv("LOGS_PATH"),
    format="API: %(name)s :: %(levelname)s :: %(message)s",
    encoding="utf-8",
    filemode="w",
)

router = APIRouter(prefix="/auth", tags=["Auth"], route_class=DishkaRoute)


@router.get("/", summary="Get all users", response_model_exclude_none=True)
async def get_all(service: FromDishka[UserService]) -> list[User]:
    try:
        results: list[User] = await service.get_all_users()
        return results
    except Exception as e:
        logging.exception(f"get_all: {str(e)}")


@router.get(
    "/{user_id}/",
    summary="Get the user by id",
    response_model_exclude_none=True,
)
async def get_user_by_id(
    user_id: int, service: FromDishka[UserService]
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
    user = await service.get_user_by_username(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    response_model=User,
    response_model_exclude_none=True,
)
async def register(
    user_input: UserInput, service: FromDishka[UserService]
) -> User:
    """
    Registers a new user in the system.
    """
    try:
        return await service.create_user(
            username=user_input.username,
            email=user_input.email,
            password=user_input.password,
        )
    except Exception as e:
        logging.exception(f"register: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    summary="Authenticate and retrieve access/refresh tokens",
    response_model=TokenResponse,
)
async def login(credentials: LoginInput, service: FromDishka[AuthService]):
    """
    Authenticates the user and returns tokens.
    """
    try:
        return await service.login(
            username=credentials.username, password=credentials.password
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        )


@router.post(
    "/logout/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout user",
)
async def logout(token: TokenData, service: FromDishka[AuthService]) -> None:
    """
    Logout the user (stateless).
    """
    try:
        await service.logout(token_data=token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token or token type",
        )


@router.post(
    "/refresh/",
    status_code=status.HTTP_200_OK,
    summary="Refresh access token using refresh token",
    response_model=TokenData,
)
async def refresh(refresh_token: TokenData, service: FromDishka[AuthService]):
    """
    Refreshes the access token.
    """
    try:
        return await service.refresh(refresh_token=refresh_token)
    except Exception as e:
        logging.exception(f"refresh: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
