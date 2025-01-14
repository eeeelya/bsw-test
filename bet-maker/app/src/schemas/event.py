from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from src.enums.status import EventStatus


class EventInfo(BaseModel):
    uuid: UUID = Field(..., description="ID канал")
    deadline: datetime = Field(..., description="Дедлайн")
    coefficient: Decimal = Field(..., description="Коэффициент")
    state: EventStatus = Field(..., description="Статус")
