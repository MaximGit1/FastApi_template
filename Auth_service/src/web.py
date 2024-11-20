from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.adapters.database.models import map_tables
from src.api import auth
from src.ioc import init_async_container


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield None
    await app.state.dishka_container.close()


def _setup_container(app: FastAPI, /) -> None:
    container = init_async_container()
    setup_dishka(container, app)


def _setup_routers(app: FastAPI, /) -> None:
    app.include_router(auth.router)


def create_app() -> FastAPI:
    app = FastAPI(lifespan=_lifespan)
    _setup_container(app)
    _setup_routers(app)
    map_tables()
    return app
