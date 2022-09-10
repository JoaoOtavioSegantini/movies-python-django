from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from _seedworker.domain.entities import Entity


@dataclass(kw_only=True, frozen=True, slots=True)  # init, repr, eq
class Category(Entity):

    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now()  # pylint: disable=unnecessary-lambda
    )

    def update(self, name: str, description: str):
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'description', description)
        return self

    def activate(self):
        object.__setattr__(self, 'is_active', True)

    def deactivate(self):
        object.__setattr__(self, 'is_active', False)
