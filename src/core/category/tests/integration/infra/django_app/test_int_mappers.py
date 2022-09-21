
import unittest
import pytest

from django.utils import timezone

from core.category.infra.django.models import CategoryModel
from core.category.infra.django.mappers import CategoryModelMapper
from core.category.domain.entities import Category


@pytest.mark.django_db
class TestCategoryModelMapper(unittest.TestCase):

    def test_to_entity(self):
        created_at = timezone.now()
        model = CategoryModel(
            id='e7ae5d8b-f322-432f-b194-2aec78d5eb28',
            name="Movie",
            description=None,
            is_active=True,
            created_at=created_at  # "2022-09-20T17:00:00Z"
        )

        entity = CategoryModelMapper.to_entity(model)

        self.assertEqual(entity.id, 'e7ae5d8b-f322-432f-b194-2aec78d5eb28')
        self.assertEqual(entity.name, 'Movie')
        self.assertIsNone(entity.description)
        self.assertTrue(entity.is_active)
        self.assertEqual(entity.created_at, created_at)

    def test_to_model(self):
        entity = Category(
            name="Movie",
            description=None,
            is_active=True
        )

        model = CategoryModelMapper.to_model(entity)

        self.assertEqual(str(model.id), entity.id)
        self.assertEqual(model.name, 'Movie')
        self.assertIsNone(model.description)
        self.assertTrue(model.is_active)
        self.assertEqual(model.created_at, entity.created_at)
