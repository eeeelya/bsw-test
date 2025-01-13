from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.http import BadRequest, NotFound
from src.models.event import Event
from src.repositories.event import EventRepository
from src.schemas.event import EventCreate, EventInfo, EventUpdate


class EventService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = EventRepository(session)

    async def get_all(self) -> list[EventInfo]:
        events: list[Event] = await self._repository.get_all()

        return [EventInfo.model_validate(event) for event in events]

    async def get(self, _id: UUID) -> EventInfo:
        event: Event | None = await self._repository.get_by_uuid(_id)

        if event is None:
            raise NotFound(detail="Мероприятие не найдено")

        return EventInfo.model_validate(event)

    async def create(self, data: EventCreate) -> EventInfo:
        event: Event = await self._repository.create(data.model_dump())

        return EventInfo.model_validate(event)

    async def update(self, _id: UUID, data: EventUpdate) -> EventInfo:
        update_data: dict = data.model_dump(exclude_none=True)

        if not update_data:
            raise BadRequest(detail="Данные для обновления не получены")

        event: Event | None = await self._repository.update_by_uuid(_id, update_data)

        if event is None:
            raise NotFound(detail="Мероприятие не найдено")

        return EventInfo.model_validate(event)
