from fastapi import APIRouter

from .users import router as users_router
from .auth import router as auth_router

global_router = APIRouter(prefix="/auth-service/api/v1")

global_router.include_router(users_router)
global_router.include_router(auth_router)

__all__ = ("global_router",)
