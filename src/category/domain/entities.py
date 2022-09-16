from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from _seedworker.domain.entities import Entity
from _seedworker.domain.exceptions import EntityValidationException
from category.domain.validators import CategoryValidatorFactory


@dataclass(kw_only=True, frozen=True, slots=True)  # init, repr, eq
class Category(Entity):

    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now()  # pylint: disable=unnecessary-lambda
    )

    def __post_init__(self):
        if not self.created_at:
            self._set('created_at',  datetime.now())
        self.validate()

    # def __new__(cls, **kwargs):
    #     cls.validate(name=kwargs.get('name'), description=kwargs.get('description'),
    #     is_active=kwargs.get('is_active'))
    #     return super(Category, cls).__new__(cls)

    def update(self, name: str, description: str):
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'description', description)
        self.validate()

        return self

    def activate(self):
        object.__setattr__(self, 'is_active', True)

    def deactivate(self):
        object.__setattr__(self, 'is_active', False)

    def validate(self):
        validator = CategoryValidatorFactory.create()
        is_valid = validator.validate(self.to_dict())
        if not is_valid:
            raise EntityValidationException(validator.errors)

    # @classmethod
    # def validate(cls, name: str, description: str, is_active: bool = None):
    #     ValidatorRules.values(name, "name").required().string().max_length(255)
    #     ValidatorRules.values(description, "description").string()
    #     ValidatorRules.values(is_active, "is_active").boolean()
