from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config.Settings import Settings

settings = Settings.get_instance()

engine = create_async_engine(
    settings.get_database_url(),
    echo=settings.SQLALCHEMY_DEBUG,
    pool_pre_ping=True
)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False
)

async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
