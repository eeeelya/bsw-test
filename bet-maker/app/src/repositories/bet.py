from src.models.bet import Bet
from src.repositories.base import BaseRepository


class BetRepository(BaseRepository[Bet]):
    model = Bet
