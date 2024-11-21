from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, status
import logging


from src.domain.models import TokenData, User, TokenResponse
from src.domain.services import UserService, AuthService
from src.adapters.schemes import UserInput, LoginInput


router = APIRouter(prefix="/auth", tags=["Auth"], route_class=DishkaRoute)


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