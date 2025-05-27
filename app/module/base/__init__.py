from fastapi import APIRouter

from .api import user

router = APIRouter()

router.include_router(user.router, prefix="/users", tags=["User"])