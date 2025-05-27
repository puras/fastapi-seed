from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Column, Integer, DateTime, String

from app.core.db import Base

class User(Base):
    """
    数据库模型
    """
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)


class UserBase(BaseModel):
    """
    HTTP交互模型
    """
    name: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True