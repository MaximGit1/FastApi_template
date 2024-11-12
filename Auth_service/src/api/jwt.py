from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from psycopg import IntegrityError
import logging

from src.adapters.schemes import UserScheme
from src.domain.models import UserDomain, GlobalPermissionDomain, Token
from src.domain.services.auth import AuthService
from src.domain.protocols import JWT_TOKEN

router = APIRouter(prefix="/auth", tags=["Auth"], route_class=DishkaRoute)

