from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from src.enums.status import EventStatus


class EventCreate(BaseModel):
    deadline: datetime = Field(..., description="Дедлайн")
    coefficient: Decimal = Field(..., ge=0, decimal_places=2, description="Коэффициент")
    state: EventStatus = Field(..., description="Статус")


class EventUpdate(BaseModel):
    deadline: datetime | None = Field(None, description="Дедлайн")
    coefficient: Decimal | None = Field(
        None, ge=0, decimal_places=2, description="Коэффициент"
    )
    state: EventStatus | None = Field(None, description="Статус")


class EventInfo(EventCreate):
    uuid: UUID = Field(..., description="ID канал")

    class Config:
        from_attributes = True
