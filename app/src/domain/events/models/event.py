from src.domain.shared.models.base import BaseSQLModel
from src.domain.shared.models.mixins.uuid import UUIDMixin


class Event(BaseSQLModel, UUIDMixin):
    pass
