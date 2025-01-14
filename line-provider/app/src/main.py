from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.events import events_router
from src.core.exceptions.handler import add_exception_handlers
from src.core.settings import env_settings
from src.infrastructure.kafka.producer import kafka_producer
from src.infrastructure.postgresql.database import db
from src.services.consumer import event_request_consumer


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    db.startup()
    await kafka_producer.setup()
    await event_request_consumer.setup()
    await event_request_consumer.start()

    yield

    await event_request_consumer.stop()
    await kafka_producer.close()
    await db.shutdown()


app = FastAPI(
    title=env_settings.LINE_PROVIDER_NAME, lifespan=lifespan, root_path="/line-provider"
)
add_exception_handlers(app)

app.include_router(events_router, prefix=env_settings.API_PREFIX)
