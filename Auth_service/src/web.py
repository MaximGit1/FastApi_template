from typing import AsyncIterator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.adapters.database.models import map_tables
from src.api import users, index
from src.ioc import init_async_container


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield None
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(users.router)
    app.include_router(index.router)
    container = init_async_container()
    setup_dishka(container, app)
    map_tables()
    return app
