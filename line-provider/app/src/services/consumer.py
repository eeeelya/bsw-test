from uuid import UUID

from aiokafka import ConsumerRecord

from src.infrastructure.kafka.commands import KafkaCommand
from src.infrastructure.kafka.consumer import AIOKafkaConsumerWrapper
from src.infrastructure.kafka.producer import kafka_producer
from src.infrastructure.kafka.topic import KafkaTopic
from src.infrastructure.postgresql.session import get_session
from src.services.event import EventService


async def exec_command(command: str, _id: str | None) -> list[dict] | dict:
    async with get_session() as session:
        service = EventService(session)

        if command == KafkaCommand.GET_ALL_EVENTS.value:
            events = await service.get_all()

            return list(map(lambda x: x.model_dump(), events))
        elif command == KafkaCommand.GET_EVENT.value:
            if not _id:
                raise ValueError

            event = await service.get(UUID(_id))

            return event.model_dump()

        raise ValueError


class EventRequestConsumer(AIOKafkaConsumerWrapper):
    @staticmethod
    async def process_message(message: ConsumerRecord) -> None:
        if not message.value:
            return None

        if not (correlation_id := message.value.get("correlation_id")):
            return None

        if not (command := message.value.get("command")):
            return None

        event_id = message.value.get("uuid")

        try:
            data = await exec_command(command, _id=event_id)
        except ValueError:
            return None

        value = {
            "correlation_id": correlation_id,
            "events": data,
        }

        await kafka_producer.send(KafkaTopic.RESPONSE.value, value)


event_request_consumer = EventRequestConsumer(
    KafkaTopic.REQUEST.value, group_id="request"
)
