from typing import List
from django.core import exceptions as django_exceptions
from core.category.domain.repositories import CategoryRepository
from core.category.domain.entities import Category
from core._seedworker.domain.entities import UniqueEntityId
from core.category.infra.django.models import CategoryModel
from core._seedworker.domain.exceptions import NotFoundException


class CategoryDjangoRepository(CategoryRepository):

    def insert(self, entity: Category) -> None:
        CategoryModel.objects.create(  # pylint: disable=no-member
            **entity.to_dict())

    def find_all(self) -> List[Category]:
        return [Category(
            unique_entity_id=UniqueEntityId(str(model.id)),
            name=model.name,
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at) for model in CategoryModel.objects.all()]  # pylint: disable=no-member

    def find_by_id(self, entity_id: str | UniqueEntityId) -> Category:
        id_str = str(entity_id)
        model = self._get(id_str)
        return Category(
            unique_entity_id=UniqueEntityId(id_str),
            name=model.name,
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at
        )

    def update(self, entity: Category) -> None:
        return super().update(entity)

    def delete(self, entity_id: str | UniqueEntityId) -> None:
        return super().delete(entity_id)

    def _get(self, entity_id: str) -> CategoryModel:
        try:
            return CategoryModel.objects.get(pk=entity_id)  # pylint: disable=no-member
        except (CategoryModel.DoesNotExist, django_exceptions.ValidationError) as ex:  # pylint: disable=no-member
            raise NotFoundException(
                f"Entity not found using ID '{entity_id}'") from ex

    def search(
        self, input_params: CategoryRepository.SearchParams
    ) -> CategoryRepository.SearchResult:
        return super().search(input_params)
