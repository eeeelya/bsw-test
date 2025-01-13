from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.settings import env_settings
from src.infrastructure.postgresql.exceptions import DatabaseIsNotInitialized


class Database:
    def __init__(self) -> None:
        self._engine: AsyncEngine | None = None
        self._session_maker: async_sessionmaker | None = None

    @property
    def session_maker(self) -> async_sessionmaker:
        if self._session_maker is None:
            raise DatabaseIsNotInitialized

        return self._session_maker

    def startup(self) -> None:
        self._engine = create_async_engine(
            env_settings.DB_URL,
            pool_size=100,
            max_overflow=20,
            echo=False,
        )
        self._session_maker = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def shutdown(self) -> None:
        if self._engine:
            await self._engine.dispose()


db = Database()
