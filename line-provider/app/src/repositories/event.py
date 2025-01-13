from src.models.event import Event
from src.repositories.base import BaseRepository


class EventRepository(BaseRepository[Event]):
    model = Event
