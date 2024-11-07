from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, status
from psycopg import IntegrityError
import logging


from src.adapters.schemes import UserScheme
from src.domain.models import UserDomain
from src.domain.services.users import UserService


router = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)


@router.get("/", summary="Get all users!")
async def get_all(service: FromDishka[UserService]) -> list[UserDomain]:
    results: list[UserDomain] = await service.get_all()
    return results


@router.get("/{user_id}/", summary="Get user by id")
async def get_by_id(
    user_id: int, service: FromDishka[UserService]
) -> UserDomain:
    result = await service.get_by_id(user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="user not found")
    return result


@router.post(
    "/create/", status_code=status.HTTP_201_CREATED, summary="Add user"
)
async def create(
    user: UserScheme, service: FromDishka[UserService]
) -> UserDomain | dict[str, str]:
    try:
        new_user = await service.create(user.to_model())
        return new_user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this nickname already exists",
        )
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")  # Логируем исключение
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user",
        ) from e


@router.put("/update/", summary="Update user")
async def update(
    user: UserScheme, service: FromDishka[UserService]
) -> dict[str, str]:
    result = await service.update(user.to_model())
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user does not exist",
        )
    return {"message": "user updated"}


@router.delete("/delete/{user_id}/", summary="Delete user")
async def delete_by_id(
    user_id: int, service: FromDishka[UserService]
) -> dict[str, str]:
    await service.delete_by_id(user_id)
    return {"message": "user has been removed"}
