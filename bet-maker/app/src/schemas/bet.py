from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from src.enums.status import EventStatus


class BetCreate(BaseModel):
    event_uuid: UUID = Field(..., description="Событие")
    amount: Decimal = Field(..., ge=0, decimal_places=2, description="Ставка")


class BetInfo(BetCreate):
    uuid: UUID = Field(..., description="ID канал")
    state: EventStatus = Field(..., description="Статус")
