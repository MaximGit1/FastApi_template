import os
from collections.abc import AsyncIterator
from typing import NewType

from dishka import (
    AnyOf,
    AsyncContainer,
    Provider,
    Scope,
    make_async_container,
    provide, FromDishka,
)

from dishka.integrations.fastapi import FastapiProvider

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from fastapi import Request

from src.adapters.database.repositories import (
    UserRepository,
    JWTRepository,
    SaltRepository,
    CookieRepository,
)
from src.domain.models import User
from src.domain.protocols import (
    JWTProtocol,
    UoWProtocol,
    SaltProtocol,
    UserDAOProtocol,
    CookieProtocol,
)
from src.domain.services import (
    UserService,
    AuthService,
    SaltService,
    CookiesService,
)


DBURI = NewType("DBURI", str)


class DBProvider(Provider):
    @provide(scope=Scope.APP)
    def db_uri(self) -> DBURI:
        db_uri = os.getenv("POSTGRES_URI")
        if db_uri is None:
            raise ValueError("POSTGRES_URI is not set")
        return DBURI(db_uri)

    @provide(scope=Scope.APP)
    async def create_engine(self, db_uri: DBURI) -> AsyncIterator[AsyncEngine]:
        engine = create_async_engine(
            db_uri,
            echo=True,
            pool_size=15,
            max_overflow=15,
            connect_args={"connect_timeout": 5},
        )
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def create_async_sessionmaker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            engine,
            autoflush=False,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)
    async def new_async_session(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AnyOf[AsyncSession, UoWProtocol]]:
        async with session_factory() as session:
            yield session


# class APIMiddleware(Provider):
#     @provide(scope=Scope.REQUEST)
#     async def get_current_user(
#             self,
#             request: Request,
#             user_service: UserService,
#             auth_service: AuthService,
#             cookie_service: CookiesService,
#     ) -> User:
#         access_token = cookie_service.get_access_token(request=request)
#         user_id = auth_service.get_user_id_by_access_token(
#             access_token=access_token
#         )
#         user = await user_service.get_user_by_id(user_id=user_id)
#         return user


def repository_provider() -> Provider:
    provider = Provider()
    provider.provide(
        UserRepository,
        scope=Scope.REQUEST,
        provides=UserDAOProtocol,
    )
    provider.provide(JWTRepository, scope=Scope.REQUEST, provides=JWTProtocol)
    provider.provide(
        SaltRepository,
        scope=Scope.REQUEST,
        provides=SaltProtocol,
    )
    provider.provide(
        CookieRepository, scope=Scope.REQUEST, provides=CookieProtocol
    )
    return provider


def service_provider() -> Provider:
    provider = Provider()
    provider.provide(AuthService, scope=Scope.REQUEST)
    provider.provide(UserService, scope=Scope.REQUEST)
    provider.provide(SaltService, scope=Scope.REQUEST)
    provider.provide(CookiesService, scope=Scope.REQUEST)
    return provider


def init_async_container() -> AsyncContainer:
    providers = [
        DBProvider(),
        # FastapiProvider(),
        repository_provider(),
        service_provider(),
        # APIMiddleware(),
    ]
    return make_async_container(*providers)
