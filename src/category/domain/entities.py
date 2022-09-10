from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from _seedworker.domain.entities import Entity


@dataclass(kw_only=True, frozen=True)  # init, repr, eq
class Category(Entity):

    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now()  # pylint: disable=unnecessary-lambda
    )
