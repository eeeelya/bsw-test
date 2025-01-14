from fastapi.routing import APIRouter

from src.infrastructure.postgresql.session import get_session
from src.schemas.bet import BetCreate, BetInfo
from src.services.bet import BetService

bets_router = APIRouter(tags=["Ставки"], prefix="/bets")


@bets_router.get(
    "/",
    name="Получить все ставки",
    description="Получить все ставки",
)
async def get_events() -> list[BetInfo]:
    async with get_session() as session:
        service = BetService(session)

        return await service.get_all()


@bets_router.post(
    "/",
    name="Сделать ставку",
    description="Сделать ставку",
)
async def get_event(data: BetCreate) -> BetInfo:
    async with get_session() as session:
        service = BetService(session)

        return await service.make(data)
