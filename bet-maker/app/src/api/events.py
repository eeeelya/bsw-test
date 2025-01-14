from uuid import UUID

from fastapi.routing import APIRouter

from src.schemas.event import EventInfo
from src.services.event import EventService

events_router = APIRouter(tags=["События"], prefix="/events")


@events_router.get(
    "/",
    name="Получить все события",
    description="Получить все события",
)
async def get_events() -> list[EventInfo]:
    service = EventService()

    return await service.get_all()


@events_router.get(
    "/{event_uuid}/",
    name="Получить событие",
    description="Получить событие",
)
async def get_event(event_uuid: UUID) -> EventInfo:
    service = EventService()

    return await service.get(event_uuid)
