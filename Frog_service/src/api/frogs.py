from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, status

from src.adapters.schemes import FrogSchema
from src.domain.models import FrogDomain
from src.domain.services.frog import FrogService


router = APIRouter(
    prefix="/frogs", tags=["Frooooooogs!"], route_class=DishkaRoute
)


@router.get("/", summary="Get all froogs!")
async def get_all(service: FromDishka[FrogService]) -> list[FrogDomain]:
    results: list[FrogDomain] = await service.get_all()
    return results


@router.get("/{id}", summary="Get froooooog by id")
async def get_by_id(id_: int, service: FromDishka[FrogService]) -> FrogDomain:
    result = await service.get_by_id(id_)
    if result is None:
        raise HTTPException(status_code=404, detail="frog not found")
    return result


@router.post("/add", status_code=status.HTTP_201_CREATED, summary="Add frog")
async def add(
    frog: FrogSchema, service: FromDishka[FrogService]
) -> dict[str, str]:
    try:
        await service.create(frog.to_model())
        return {"message": "frog created :)"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"frog already exists {e}",
        ) from e


@router.put("/update", summary="Update frog")
async def update(
    frog: FrogSchema, service: FromDishka[FrogService]
) -> dict[str, str]:
    await service.update(frog.to_model())
    return {"message": "fr0_--g updated"}


@router.delete("/delete/{id}", summary="Delete frog by id😓")
async def delete_by_id(
    id_: int, service: FromDishka[FrogService]
) -> dict[str, str]:
    await service.delete_by_id(id_)
    return {"message": "frog deleted"}
