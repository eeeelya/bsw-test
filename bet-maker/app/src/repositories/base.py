from collections.abc import Sequence
from typing import Generic, Protocol, TypeVar
from uuid import UUID

from sqlalchemy import Delete, Select, Update, delete, select, update
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped


class BaseModelProtocol(Protocol):
    uuid: Mapped[UUID]


T = TypeVar("T", bound=BaseModelProtocol)


class BaseRepository(Generic[T]):
    model: type[T]

    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def get_by_uuid(self, _uuid: UUID) -> T | None:
        stmt: Select = select(self.model).where(self.model.uuid == _uuid)

        result = await self._session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_many_by_uuids(self, uuids: Sequence[UUID]) -> list[T] | None:
        stmt: Select = select(self.model).where(self.model.uuid.in_(uuids))

        result = await self._session.execute(stmt)

        return list(result.scalars().all())

    async def get_all(self) -> list[T]:
        stmt: Select = select(self.model)

        result = await self._session.execute(stmt)

        return list(result.scalars().all())

    async def create(self, data: dict) -> T:
        _object: T = self.model(**data)

        self._session.add(_object)
        await self._session.flush()

        return _object

    async def create_many(self, data: Sequence[dict]) -> list[T]:
        _objects: list[T] = [self.model(**item) for item in data]

        self._session.add_all(_objects)
        await self._session.flush()

        return _objects

    async def update_by_uuid(self, _uuid: UUID, data: dict) -> T | None:
        stmt: Update = (
            update(self.model)
            .where(self.model.uuid == _uuid)
            .values(**data)
            .returning(self.model)
        )

        result: Result = await self._session.execute(stmt)
        await self._session.flush()

        return result.scalar_one_or_none()

    async def update_many_by_uuids(self, uuids: Sequence[UUID], data: dict) -> list[T]:
        stmt: Update = (
            update(self.model)
            .where(self.model.uuid.in_(uuids))
            .values(data)
            .returning(self.model)
        )

        result: Result = await self._session.execute(stmt)
        await self._session.flush()

        return list(result.scalars().all())

    async def delete_by_uuid(self, _uuid: UUID) -> bool:
        stmt: Delete = delete(self.model).where(self.model.uuid == _uuid)

        result: CursorResult = await self._session.execute(stmt)
        await self._session.flush()

        return bool(result.rowcount)

    async def delete_many_by_uuids(self, uuids: list[UUID]) -> int:
        stmt: Delete = delete(self.model).where(self.model.uuid.in_(uuids))

        result: CursorResult = await self._session.execute(stmt)
        await self._session.flush()

        return result.rowcount
