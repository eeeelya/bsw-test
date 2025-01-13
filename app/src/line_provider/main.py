from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.settings import env_settings
from src.line_provider.api.events import events_router

# from src.infrastructure.postgresql.engines import close_db_engines, init_db_engines


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # await init_db_engines()
    # await kafka_producer.setup()

    yield

    # await kafka_producer.close()
    # await close_db_engines()


app = FastAPI(
    title=env_settings.LINE_PROVIDER_NAME, lifespan=lifespan, root_path="/line-provider"
)
# add_exception_handlers(app)

app.include_router(events_router, prefix=env_settings.API_PREFIX)
