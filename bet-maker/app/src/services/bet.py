from sqlalchemy.ext.asyncio import AsyncSession

from src.models.bet import Bet
from src.repositories.bet import BetRepository
from src.schemas.bet import BetCreate, BetInfo
from src.schemas.event import EventInfo
from src.services.event import EventService


class BetService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = BetRepository(session)

        self._events = EventService()

    async def _get_info(self, instance: Bet) -> BetInfo:
        event: EventInfo = await self._events.get(instance.event_uuid)

        return BetInfo(
            uuid=instance.uuid,
            amount=instance.amount,
            event_uuid=instance.event_uuid,
            state=event.state,
        )

    async def get_all(self) -> list[BetInfo]:
        bets: list[Bet] = await self._repository.get_all()

        return [await self._get_info(bet) for bet in bets]

    async def make(self, data: BetCreate) -> BetInfo:
        bet: Bet = await self._repository.create(data.model_dump())

        return await self._get_info(bet)
