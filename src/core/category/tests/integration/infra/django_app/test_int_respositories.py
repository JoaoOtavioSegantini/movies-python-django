#pylint: disable=no-member

import unittest
import pytest
from model_bakery import baker
from core.category.infra.django.repositories import CategoryDjangoRepository
from core.category.infra.django.models import CategoryModel
from core.category.infra.django.mappers import CategoryModelMapper
from core.category.domain.entities import Category
from core._seedworker.domain.exceptions import NotFoundException
from core._seedworker.domain.entities import UniqueEntityId


@pytest.mark.django_db()
class TestCategoryDjangoRepositoryInt(unittest.TestCase):

    repo: CategoryDjangoRepository

    def setUp(self) -> None:
        self.repo = CategoryDjangoRepository()

    def test_insert(self):
        category = Category(name="Movie")
        self.repo.insert(category)

        model = CategoryModel.objects.get(pk=category.id)

        self.assertEqual(str(model.id), category.id)
        self.assertEqual(model.name, category.name)
        self.assertIsNone(model.description)
        self.assertTrue(model.is_active)
        self.assertEqual(model.created_at, category.created_at)

        category = Category(
            name="Movie", description="some description", is_active=False)

        self.repo.insert(category)

        model = CategoryModel.objects.get(pk=category.id)

        self.assertEqual(str(model.id), category.id)
        self.assertEqual(model.name, category.name)
        self.assertEqual(model.description, category.description)
        self.assertFalse(model.is_active)
        self.assertEqual(model.created_at, category.created_at)

    def test_throw_not_found_exception_in_find_by_id(self):
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id('fake id')
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'fake id'")

        unique_entity_id = UniqueEntityId(
            'af46842e-027d-4c91-b259-3a3642144ba4')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.find_by_id(unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID 'af46842e-027d-4c91-b259-3a3642144ba4'"
        )

    def test_find_by_id(self):
        entity = Category(name="Movie")
        self.repo.insert(entity)

        entity_found = self.repo.find_by_id(entity.id)
        self.assertEqual(entity_found, entity)

        entity_found = self.repo.find_by_id(entity.unique_entity_id)
        self.assertEqual(entity_found, entity)

    def test_find_all(self):
        models = baker.make(CategoryModel, _quantity=2)

        categories = self.repo.find_all()

        self.assertEqual(len(categories), 2)
        self.assertEqual(
            categories[0], CategoryModelMapper.to_entity(models[0]))
        self.assertEqual(
            categories[1], CategoryModelMapper.to_entity(models[1]))

    def test_update(self):

        category = Category(name="Movie")
        self.repo.insert(category)

        category.update(name="Movie changed",
                        description="Description changed")
        self.repo.update(category)

        model = CategoryModel.objects.get(pk=category.id)
        self.assertEqual(str(model.id), category.id)
        self.assertEqual(model.name, "Movie changed")
        self.assertEqual(model.description, "Description changed")
        self.assertTrue(model.is_active)
        self.assertEqual(model.created_at, category.created_at)

    def test_throw_not_found_exception_in_delete(self):
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete('fake id')
        self.assertEqual(
            assert_error.exception.args[0], "Entity not found using ID 'fake id'")

        unique_entity_id = UniqueEntityId(
            'af46842e-027d-4c91-b259-3a3642144ba4')
        with self.assertRaises(NotFoundException) as assert_error:
            self.repo.delete(unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID 'af46842e-027d-4c91-b259-3a3642144ba4'"
        )

    def test_delete(self):

        category = Category(name="Movie")
        self.repo.insert(category)

        self.repo.delete(category.id)

        with self.assertRaises(NotFoundException):
            self.repo.find_by_id(category.id)

        with self.assertRaises(NotFoundException):
            self.repo.find_by_id(category.unique_entity_id)
