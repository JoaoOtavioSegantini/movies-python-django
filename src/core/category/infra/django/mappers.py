#pylint: disable=no-member,no-self-argument

from core.category.infra.django.models import CategoryModel
from core.category.domain.entities import Category
from core._seedworker.domain.entities import UniqueEntityId
from core._seedworker.domain.exceptions import LoadEntityException, EntityValidationException


class CategoryModelMapper:

    @staticmethod
    def to_entity(model: CategoryModel) -> Category:
        try:
            return Category(
                unique_entity_id=UniqueEntityId(str(model.id)),
                name=model.name,
                description=model.description,
                is_active=model.is_active,
                created_at=model.created_at
            )
        except EntityValidationException as ex:
            raise LoadEntityException(ex.error) from ex

    @staticmethod
    def to_model(entity: Category) -> CategoryModel:
        return CategoryModel(**entity.to_dict())
