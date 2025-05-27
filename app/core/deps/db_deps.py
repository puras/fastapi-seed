from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话依赖
    :return:
    """
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()