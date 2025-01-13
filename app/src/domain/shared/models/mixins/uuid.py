import uuid as pyUUID

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column


class UUIDMixin:
    uuid: Mapped[pyUUID.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=pyUUID.uuid4,
    )
