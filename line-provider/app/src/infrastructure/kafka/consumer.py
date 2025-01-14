import asyncio
import json
import logging
import traceback
from asyncio import Task
from typing import Any

from aiokafka import AIOKafkaConsumer, ConsumerRecord, errors

from src.core.settings import env_settings
from src.infrastructure.kafka.exceptions import KafkaDidNotStarted

logger = logging.getLogger("AIOKafkaConsumerWrapper")


class AIOKafkaConsumerWrapper:
    def __init__(self, topic: str, group_id: str) -> None:
        self._topic: str = topic
        self._group_id: str = group_id

        self._consumer: AIOKafkaConsumer | None = None
        self._task: Task | None = None

    async def setup(self) -> None:
        params: dict = dict(
            bootstrap_servers=env_settings.KAFKA_NODES,
            group_id=f"{self._group_id}",
            enable_auto_commit=False,
            auto_offset_reset="earliest",
            key_deserializer=bytes.decode,
            value_deserializer=lambda v: json.loads(v.decode()),
        )

        consumer: AIOKafkaConsumer = AIOKafkaConsumer(**params)

        try:
            await consumer.start()
        except errors.KafkaConnectionError:
            raise KafkaDidNotStarted

        logger.info(f"Start consumer: {self._topic}")

        self._consumer = consumer

    @staticmethod
    async def process_message(message: ConsumerRecord) -> None:
        raise NotImplementedError

    async def _consume_one_message(self) -> None:
        if self._consumer is None:
            raise KafkaDidNotStarted

        message: ConsumerRecord = await self._consumer.getone()

        try:
            await self.process_message(message)
        except Exception as e:
            error_path: str = "".join(traceback.format_tb(e.__traceback__))
            logger.error(
                f"Key: {message.key}.\nTopic: {message.topic}."
                f"\nTraceback: {error_path}.\nError: {e}"
            )
        finally:
            await self._consumer.commit(message.offset)

    async def consume(self) -> Any:
        if self._consumer is None:
            raise KafkaDidNotStarted

        try:
            while True:
                await self._consume_one_message()
        finally:
            await self._consumer.commit()
            await self._consumer.stop()

    async def start(self):
        self._task = asyncio.create_task(self.consume())

    async def stop(self) -> None:
        if self._consumer is not None:
            await self._consumer.commit()
            await self._consumer.stop()

        if self._task is not None:
            self._task.cancel()
