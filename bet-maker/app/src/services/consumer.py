from uuid import UUID

from aiokafka import ConsumerRecord
from pydantic_core import ValidationError

from src.infrastructure.kafka.consumer import AIOKafkaConsumerWrapper
from src.infrastructure.kafka.topic import KafkaTopic
from src.schemas.event import EventInfo


class EventResponseConsumer(AIOKafkaConsumerWrapper):
    @staticmethod
    async def process_message(
        message: ConsumerRecord, _id: UUID
    ) -> list[EventInfo] | EventInfo | None:
        if not message.value:
            return None

        if not (correlation_id := message.value.get("correlation_id")):
            return None

        event_info: dict = message.value.get("events", {})

        if correlation_id == _id:
            try:
                if isinstance(event_info, list):
                    return [EventInfo(**event) for event in event_info]

                return EventInfo(**event_info)
            except ValidationError:
                return None


event_response_consumer = EventResponseConsumer(
    KafkaTopic.RESPONSE.value, group_id="response"
)
