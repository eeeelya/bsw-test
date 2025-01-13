from datetime import datetime
from decimal import Decimal

from sqlalchemy import DECIMAL, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.enums.status import EventStatus
from src.models.base import BaseSQLModel
from src.models.mixins.uuid import UUIDMixin


class Event(BaseSQLModel, UUIDMixin):
    __tablename__ = "events"

    coefficient: Mapped[Decimal] = mapped_column(DECIMAL(scale=2), nullable=False)
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    state: Mapped[EventStatus] = mapped_column(
        server_default=EventStatus.NEW, nullable=False
    )
