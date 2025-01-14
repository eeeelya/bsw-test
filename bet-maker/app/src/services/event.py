from typing import TypedDict
from uuid import UUID, uuid4

from src.core.exceptions.http import BadRequest
from src.infrastructure.kafka.commands import KafkaCommand
from src.infrastructure.kafka.producer import kafka_producer
from src.infrastructure.kafka.topic import KafkaTopic
from src.schemas.event import EventInfo
from src.services.consumer import event_response_consumer


class RequestAllData(TypedDict):
    correlation_id: str
    command: str


class RequestData(RequestAllData):
    uuid: str | None


class EventService:
    async def _get(
        self, request_data: RequestData | RequestAllData
    ) -> list[EventInfo] | EventInfo:
        print(request_data)
        await kafka_producer.send(KafkaTopic.REQUEST.value, value=request_data)

        await event_response_consumer.setup()

        try:
            _id = UUID(request_data["correlation_id"])

            while True:
                if events := await event_response_consumer.consume(_id):
                    return events
        finally:
            await event_response_consumer.stop()

    async def get_all(self) -> list[EventInfo]:
        request_data = RequestAllData(
            command=KafkaCommand.GET_ALL_EVENTS.value,
            correlation_id=str(uuid4()),
        )

        info = await self._get(request_data)

        if isinstance(info, list):
            return info

        raise BadRequest

    async def get(self, _id: UUID) -> EventInfo:
        request_data = RequestData(
            command=KafkaCommand.GET_ALL_EVENTS.value,
            correlation_id=str(uuid4()),
            uuid=str(_id),
        )

        info = await self._get(request_data)

        if isinstance(info, EventInfo):
            return info

        raise BadRequest
