import os
from typing import List

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    # 基础配置
    PROJECT_NAME: str = "EUCP-MOSS"
    PROJECT_DESCRIPTION: str = ""
    VERSION: str = "0.1.0"
    DEBUG: bool = True

    # API配置
    API_V1_STR: str = "/api/v1"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = os.getenv("PORT", 8000)
    WORKERS: int = 4

    # 安全配置
    ALLOWED_ORIGINS: List[str] = [
        "*",
    ]

    # 数据库配置
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///./instance/moss.db"  # 使用异步SQLite驱动
    )
    DB_TABLE_PREFIX = os.getenv(
        "DB_TABLE_PREFIX",
        "mo_"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
