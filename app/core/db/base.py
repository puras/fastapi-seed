from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr

from app.conf import settings


class Base:
    @declared_attr
    def __tablename__(cls):
        return f"{settings.DB_TABLE_PREFIX}{cls.__name__.lower()}"

Base = declarative_base(cls=Base)