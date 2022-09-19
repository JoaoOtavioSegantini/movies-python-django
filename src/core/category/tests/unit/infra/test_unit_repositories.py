

import unittest
from core.category.infra.in_memory.repositories import CategoryInMemoryRepository
from core.category.domain.entities import Category


class TestCategoryInfraRepositoryUnit(unittest.TestCase):

    repo: CategoryInMemoryRepository

    def setUp(self) -> None:
        self.repo = CategoryInMemoryRepository()

    def test_repository_if_no_params_is_passed(self):

        items = [
            Category(name="Movies"),
            Category(name="Sports"),
            Category(name="Animation")
        ]

        # pylint: disable=protected-access
        items_filtered = self.repo._apply_filter(items, None)

        self.assertEqual(items_filtered, items)

    def test_repository_if_filter_param_is_passed(self):

        items = [
            Category(name="Movies"),
            Category(name="Sports"),
            Category(name="Animation")
        ]

        # pylint: disable=protected-access
        items_filtered = self.repo._apply_filter(items, "S")

        self.assertEqual(items_filtered, [items[0], items[1]])

        items_filtered = self.repo._apply_filter(items, "MOVIES")

        self.assertEqual(items_filtered, [items[0]])

    def test_repository_when_filter_params_is_passed_if_return_empty_list(self):

        items = [
            Category(name="Movies"),
            Category(name="Sports"),
            Category(name="Animation")
        ]

        # pylint: disable=protected-access
        items_filtered = self.repo._apply_filter(items, "d")
        self.assertEqual(items_filtered, [])

    def test_repository_sort_whith_default_configuration(self):

        items = [
            Category(name="Movies"),
            Category(name="Sports"),
            Category(name="Animation")
        ]

        # pylint: disable=protected-access
        items_sorted = self.repo._apply_sort(items, None, None)

        self.assertEqual(items_sorted, [items[2], items[1], items[0]])

    def test_sort_by_name(self):

        items = [
            Category(name='c'),
            Category(name='b'),
            Category(name='a'),
        ]

        # pylint: disable=protected-access
        items_sorted = self.repo._apply_sort(items, "name", "asc")
        self.assertListEqual(items_sorted, [items[2], items[1], items[0]])

        # pylint: disable=protected-access
        items_sorted = self.repo._apply_sort(items, "name", "desc")
        self.assertListEqual(items_sorted, [items[0], items[1], items[2]])
