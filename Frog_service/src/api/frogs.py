from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, status

from src.adapters.schemes import FrogSchema
from src.domain.models import FrogDomain
from src.domain.services.frog import FrogService


router = APIRouter(
    prefix="/frogs", tags=["Frooooooogs!"], route_class=DishkaRoute
)


@router.get("/", summary="Get all frooogs!")
async def get_all(service: FromDishka[FrogService]) -> list[FrogDomain]:
    results: list[FrogDomain] = await service.get_all()
    return results


@router.get("/{id}/", summary="Get froooooog by id")
async def get_by_id(id_: int, service: FromDishka[FrogService]) -> FrogDomain:
    result = await service.get_by_id(id_)
    if result is None:
        raise HTTPException(status_code=404, detail="frog not found")
    return result


@router.post(
    "/create/", status_code=status.HTTP_201_CREATED, summary="Add frog"
)
async def create(
    frog: FrogSchema, service: FromDishka[FrogService]
) -> FrogDomain | dict[str, str]:
    try:
        new_frog = await service.create(frog.to_model())
        return new_frog
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="frog already exists",
        ) from e


@router.put("/update/", summary="Update froooog")
async def update(
    frog: FrogSchema, service: FromDishka[FrogService]
) -> dict[str, str]:
    await service.update(frog.to_model())
    return {"message": "frog updated"}


@router.delete("/delete/{id}/", summary="Delete frog by id😓")
async def delete_by_id(
    id_: int, service: FromDishka[FrogService]
) -> dict[str, str]:
    await service.delete_by_id(id_)
    return {"message": "frog deleted"}
