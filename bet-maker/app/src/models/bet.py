import uuid
from decimal import Decimal

from sqlalchemy import DECIMAL, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseSQLModel
from src.models.mixins.uuid import UUIDMixin


class Bet(BaseSQLModel, UUIDMixin):
    __tablename__ = "bets"

    event_uuid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(scale=2), nullable=False)
