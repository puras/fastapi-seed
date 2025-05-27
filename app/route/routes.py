from fastapi import APIRouter

from app import api
from app.module import base

api_router = APIRouter()

def create_routes():
    # 系统默认
    api_router.include_router(api.router, prefix="", tags=["api"])

    # Base
    api_router.include_router(base.router, prefix="/base", tags=["base"])

    return api_router