

from abc import ABC
from _seedworker.domain.repositories import RepositoryInterface
from category.domain.entities import Category


class CategoryRepository(RepositoryInterface[Category], ABC):
    pass
