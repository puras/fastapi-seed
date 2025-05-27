from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def hello():
    return {
        "code": 0,
        "message": "Hello World!",
        "data": None
    }