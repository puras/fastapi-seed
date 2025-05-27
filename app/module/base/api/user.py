import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.response import BaseResponse, res_ok
from app.module.base.biz.user import get_users, create_user
from app.module.base.model.user import UserInDB, UserCreate

router = APIRouter()

@router.get("", response_model=BaseResponse[List[UserInDB]])
async def user_list(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    ret = await get_users(db, skip, limit)
    return res_ok(data=ret)

@router.post("", response_model=BaseResponse[UserInDB])
async def user_create(
        user: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    logging.info(f"Create user {user}")
    ret = await create_user(db, user)
    return res_ok(data=ret)