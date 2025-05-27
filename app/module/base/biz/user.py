from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.base.model.user import UserCreate, User


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    ret = await db.execute(
        select(User)
        .offset(skip)
        .limit(limit)
    )
    return ret.scalars().all()

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user