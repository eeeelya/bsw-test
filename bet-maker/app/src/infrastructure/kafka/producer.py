import json
import logging
import uuid
from typing import Any

from aiokafka import AIOKafkaProducer, errors

from src.core.settings import env_settings
from src.infrastructure.kafka.exceptions import KafkaDidNotStarted

logger: logging.Logger = logging.getLogger("KAFKA_PRODUCER")


class _AIOKafkaProducer(AIOKafkaProducer):
    async def send(
        self,
        topic,
        value=None,
        key=None,
        partition=None,
        timestamp_ms=None,
        headers=None,
    ):  # type:ignore
        key_: str = uuid.uuid4().hex

        return await super().send(topic, value, key_, partition, timestamp_ms, headers)


class AIOKafkaProducerWrapper:
    def __init__(self) -> None:
        self._producer: _AIOKafkaProducer | None = None

    async def setup(self) -> None:
        if self._producer is None:
            self._producer = _AIOKafkaProducer(
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
