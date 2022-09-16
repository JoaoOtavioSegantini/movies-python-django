from typing import List
from category.domain.repositories import CategoryRepository
from category.domain.entities import Category
from _seedworker.domain.repositories import InMemorySearchableRepository


class CategoryInMemoryRepository(CategoryRepository, InMemorySearchableRepository):
    sortable_fields: List[str] = ["name", "created_at"]

    def _apply_filter(self, items: List[Category], filter_param: str = None) -> List[Category]:
        if filter_param:
            filtered_items = filter(
                lambda item: filter_param.lower() in item.name.lower(), items)
            return list(filtered_items)
        return items

    def _apply_sort(
        self,
        items: List[Category],
        sort: str = None,
        sort_dir: str = None
    ) -> List[Category]:
        return super()._apply_sort(items, sort, sort_dir) if sort \
            else super()._apply_sort(items, "created_at", "desc")
