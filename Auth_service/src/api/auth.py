from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, status, Response, Request
import logging


from src.domain.models import AccessToken, RefreshToken, User, UserID
from src.domain.services import AuthService, UserService, CookiesService
from src.adapters.schemes import UserLoginInput, UserRegisterInput

router = APIRouter(prefix="/auth", tags=["Auth"], route_class=DishkaRoute)


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


@router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    summary="Authenticate and retrieve access token",
)
async def login(
    response: Response,
    user_data: UserLoginInput,
    user_service: FromDishka[UserService],
    auth_service: FromDishka[AuthService],
    cookie_service: FromDishka[CookiesService],
) -> None:
    user: User = await user_service.authenticate_user(
        username=user_data.username, password=user_data.password
    )
    access_token = auth_service.login_user(user=user)
    cookie_service.set_set_access_token(
        value=access_token.token, response=response
    )


#
#
# @router.post(
#     "/refresh/",
#     status_code=status.HTTP_200_OK,
#     summary="Refresh access token using refresh token",
#     response_model=TokenData,
# )
# async def refresh(refresh_token: TokenData, service: FromDishka[AuthService]):
#     """
#     Refreshes the access token.
#     """
#     try:
#         return await service.refresh(refresh_token=refresh_token)
#     except Exception as e:
#         logging.exception(f"refresh: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
#         )
#
@router.post(
    "/logout/",
    summary="Logout user",
)
async def logout(
    response: Response, service: FromDishka[CookiesService]
) -> None:
    service.delete_access_token(response=response)
