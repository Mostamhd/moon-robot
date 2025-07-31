from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.robot.core.config import settings

# Create async engine
engine = create_async_engine(
    settings.database_url, pool_size=5, max_overflow=10, pool_recycle=3600, echo=False
)

# Create async session factory
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Base class for our models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting a database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
