import json
import logging
from typing import Any

from aiokafka import AIOKafkaProducer, errors

from src.core.settings import env_settings
from src.infrastructure.kafka.exceptions import KafkaDidNotStarted

logger: logging.Logger = logging.getLogger("KAFKA_PRODUCER")


class AIOKafkaProducerWrapper:
    def __init__(self) -> None:
        self._producer: AIOKafkaProducer | None = None

    async def setup(self) -> None:
        if self._producer is None:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=env_settings.KAFKA_NODES,
                acks="all",
                key_serializer=str.encode,
                value_serializer=lambda x: json.dumps(x).encode(),
            )

            try:
                await self._producer.start()

                logger.info("Producer setup completed.")
            except errors.KafkaConnectionError as e:
                logger.error(f"Failed to start producer: {e}")

    async def send(self, topic: str, value: Any) -> None:
        if self._producer is None:
            raise KafkaDidNotStarted

        await self._producer.send_and_wait(topic=topic, value=value)

    async def close(self) -> None:
        if self._producer is not None:
            await self._producer.stop()


kafka_producer: AIOKafkaProducerWrapper = AIOKafkaProducerWrapper()
