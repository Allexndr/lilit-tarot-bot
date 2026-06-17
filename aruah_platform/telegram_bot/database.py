"""
Модуль для работы с базой данных
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings
from telegram_bot.models import Base


# Создание async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True
)

# Создание session factory
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    """Получить сессию базы данных"""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Инициализация таблиц базы данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Закрытие соединений с базой данных"""
    await engine.dispose()


class DatabaseManager:
    """Менеджер для работы с базой данных"""
    
    @staticmethod
    async def get_session() -> AsyncSession:
        return async_session_factory()
    
    @staticmethod
    async def execute_in_session(func, *args, **kwargs):
        """Выполнить функцию в сессии базы данных"""
        async with async_session_factory() as session:
            try:
                result = await func(session, *args, **kwargs)
                await session.commit()
                return result
            except Exception as e:
                await session.rollback()
                raise e

