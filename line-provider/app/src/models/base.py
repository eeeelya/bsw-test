from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase


class BaseSQLModel(DeclarativeBase):
    __abstract__ = True

    def as_dict(self) -> dict:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
