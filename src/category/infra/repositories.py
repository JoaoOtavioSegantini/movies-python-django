from category.domain.repositories import CategoryRepository
from _seedworker.domain.repositories import InMemoryRepository


class CategoryInMemoryRepository(CategoryRepository, InMemoryRepository):
    pass
