from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.bet_maker.api.bets import bets_router
from src.bet_maker.api.events import events_router
from src.core.settings import env_settings

# from src.infrastructure.postgresql.engines import close_db_engines, init_db_engines


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # await init_db_engines()
    # await kafka_producer.setup()

    yield

    # await kafka_producer.close()
    # await close_db_engines()


app = FastAPI(
    title=env_settings.BET_MAKER_NAME, lifespan=lifespan, root_path="/bet-maker"
)
# add_exception_handlers(app)

app.include_router(bets_router, prefix=env_settings.API_PREFIX)
app.include_router(events_router, prefix=env_settings.API_PREFIX)
