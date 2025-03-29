from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from src.settings import settings


class DBConfig:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine: AsyncEngine = create_async_engine(url=url, echo=echo)
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine
        )

    # Method to close the database engine for life cycle management
    async def dispose(self) -> None:
        """close database engine"""
        await self.engine.dispose()

    # Method for Dependency Injection
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session

    # Get the engine for the database
    def get_engine(self) -> AsyncEngine:
        return self.engine


# Initialize the database configuration
db_config = DBConfig(settings.DB_URL, settings.DB_ECHO)
