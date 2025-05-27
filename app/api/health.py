from fastapi import APIRouter

from app.conf import settings

router = APIRouter()

@router.get("/health")
async def health():
    return {
        "code": 200,
        "message": "success",
        "data": {
            "status": "healthy",
            "version": settings.VERSION
        }
    }