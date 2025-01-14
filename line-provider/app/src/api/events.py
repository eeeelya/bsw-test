from uuid import UUID

from fastapi.routing import APIRouter

from src.infrastructure.postgresql.session import get_session
from src.schemas.event import EventCreate, EventInfo, EventUpdate
from src.services.event import EventService

events_router = APIRouter(tags=["События"], prefix="/events")


@events_router.get(
    "/",
    name="Получить все события",
    description="Получить все события",
)
async def get_events() -> list[EventInfo]:
    async with get_session() as session:
        service = EventService(session)

        return await service.get_all()


@events_router.get(
    "/{event_uuid}/",
    name="Получить событие",
    description="Получить событие",
)
async def get_event(event_uuid: UUID) -> EventInfo:
    async with get_session() as session:
        service = EventService(session)

        return await service.get(event_uuid)


@events_router.post(
    "/",
    name="Создать событие",
    description="Создать событие",
)
async def create_event(data: EventCreate) -> EventInfo:
    async with get_session() as session:
        service = EventService(session)

        return await service.create(data)


@events_router.patch(
    "/{event_uuid}/",
    name="Обновить событие",
    description="Обновить событие",
)
async def update_event(event_uuid: UUID, data: EventUpdate) -> EventInfo:
    async with get_session() as session:
        service = EventService(session)

        return await service.update(event_uuid, data)
