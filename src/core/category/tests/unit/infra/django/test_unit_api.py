

from datetime import datetime
import unittest
from unittest import mock
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from core.category.infra.django.api import CategoryResource
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    ListCategoriesUseCase,
    GetCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase
)


class TestCategoryResourceUnit(unittest.TestCase):

    def test_post_method(self):

        send_data = {'name': "Movie"}

        created_at = datetime.now()

        mock_create_use_case = mock.Mock(CreateCategoryUseCase)

        mock_create_use_case.execute.return_value = CreateCategoryUseCase.Output(
            id='e7ae5d8b-f322-432f-b194-2aec78d5eb28',
            name=send_data['name'],
            description=None,
            is_active=True,
            created_at=created_at
        )

        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'create_use_case': lambda: mock_create_use_case
            })

        _request = APIRequestFactory().post('/', send_data)
        request = Request(_request)
        request._full_data = send_data  # pylint: disable=protected-access
        response = resource.post(request)

        mock_create_use_case.execute.assert_called_with(
            CreateCategoryUseCase.Input(name='Movie'))

        self.assertEqual(response.status_code, 201)

        self.assertEqual(response.data, {
            'id': 'e7ae5d8b-f322-432f-b194-2aec78d5eb28',
            'name': 'Movie',
            'description': None,
            'is_active': True,
            'created_at': created_at
        })

    def test_list_method(self):
        created_at = datetime.now()

        mock_list_use_case = mock.Mock(ListCategoriesUseCase)

        mock_list_use_case.execute.return_value = ListCategoriesUseCase.Output(
            items=[
                CreateCategoryUseCase.Output(
                    id='e7ae5d8b-f322-432f-b194-2aec78d5eb28',
                    name='Movie',
                    description=None,
                    is_active=True,
                    created_at=created_at
                )
            ],
            total=1,
            current_page=1,
            per_page=2,
            last_page=1
        )

        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'list_use_case': lambda: mock_list_use_case
            })

        _request = APIRequestFactory().get(
            '/?page=1&per_page=1&sort=name&sort_dir=asc&filter=test')
        request = Request(_request)
        response = resource.get(request)

        mock_list_use_case.execute.assert_called_with(
            ListCategoriesUseCase.Input(
                page='1',
                per_page='1',
                sort='name',
                sort_dir='asc',
                filter='test'
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data, {
            'items': [
                {
                    'id': 'e7ae5d8b-f322-432f-b194-2aec78d5eb28',
                    'name': 'Movie',
                    'description': None,
                    'is_active': True,
                    'created_at': created_at
                }
            ],
            'current_page': 1,
            'last_page': 1,
            'per_page': 2,
            'total': 1
        })

    def test_if_get_invoke_get_object(self):
        created_at = datetime.now()
        mock_list_use_case = mock.Mock(ListCategoriesUseCase)

        mock_get_use_case = mock.Mock(GetCategoryUseCase)
        mock_get_use_case.execute.return_value = GetCategoryUseCase.Output(
            id='e7ae5d8b-f322-432f-b194-2aec78d5eb28',
            name='Movie',
            description=None,
            is_active=True,
            created_at=created_at
        )

        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'get_use_case': lambda: mock_get_use_case,
                'list_use_case': lambda: mock_list_use_case
            })

        response = resource.get(None, 'e7ae5d8b-f322-432f-b194-2aec78d5eb28')
        self.assertEqual(mock_list_use_case.call_count, 0)
        mock_get_use_case.execute.assert_called_with(
            GetCategoryUseCase.Input(
                id="e7ae5d8b-f322-432f-b194-2aec78d5eb28"
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data, {
            'id': 'e7ae5d8b-f322-432f-b194-2aec78d5eb28',
            'name': 'Movie',
            'description': None,
            'is_active': True,
            'created_at': created_at
        })

    def test_get_category_by_id_method(self):
        created_at = datetime.now()

        mock_get_use_case = mock.Mock(GetCategoryUseCase)

        mock_get_use_case.execute.return_value = GetCategoryUseCase.Output(
            id='e7ae5d8b-f322-432f-b194-2aec78d5eb28',
            name='Movie',
            description=None,
            is_active=True,
            created_at=created_at
        )

        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'get_use_case': lambda: mock_get_use_case
            })

        response = resource.get_object('e7ae5d8b-f322-432f-b194-2aec78d5eb28')

        mock_get_use_case.execute.assert_called_with(
            GetCategoryUseCase.Input(
                id="e7ae5d8b-f322-432f-b194-2aec78d5eb28"
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data, {
            'id': 'e7ae5d8b-f322-432f-b194-2aec78d5eb28',
            'name': 'Movie',
            'description': None,
            'is_active': True,
            'created_at': created_at
        })

    def test_put_method(self):
        created_at = datetime.now()
        send_data = {'name': "Movie"}

        mock_update_use_case = mock.Mock(UpdateCategoryUseCase)

        mock_update_use_case.execute.return_value = UpdateCategoryUseCase.Output(
            id='e7ae5d8b-f322-432f-b194-2aec78d5eb28',
            name='Movie',
            description=None,
            is_active=True,
            created_at=created_at
        )

        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'update_use_case': lambda: mock_update_use_case
            })

        _request = APIRequestFactory().put('/', send_data)
        request = Request(_request)
        request._full_data = send_data  # pylint: disable=protected-access
        response = resource.put(
            request, 'e7ae5d8b-f322-432f-b194-2aec78d5eb28')
        mock_update_use_case.execute.assert_called_with(
            UpdateCategoryUseCase.Input(
                id="e7ae5d8b-f322-432f-b194-2aec78d5eb28",
                name='Movie'
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data, {
            'id': 'e7ae5d8b-f322-432f-b194-2aec78d5eb28',
            'name': 'Movie',
            'description': None,
            'is_active': True,
            'created_at': created_at
        })

    def test_delete_method(self):

        mock_delete_use_case = mock.Mock(DeleteCategoryUseCase)

        mock_delete_use_case.execute.return_value = None

        resource = CategoryResource(
            **{
                **self.__init_all_none(),
                'delete_use_case': lambda: mock_delete_use_case
            })

        _request = APIRequestFactory().delete('/')
        request = Request(_request)
        response = resource.delete(
            request, 'e7ae5d8b-f322-432f-b194-2aec78d5eb28'
        )

        mock_delete_use_case.execute.assert_called_with(
            DeleteCategoryUseCase.Input(
                id="e7ae5d8b-f322-432f-b194-2aec78d5eb28"
            )
        )

        self.assertEqual(response.status_code, 204)

        self.assertEqual(response.data, None)

    def __init_all_none(self):
        return {
            'create_use_case': None,
            'list_use_case': None,
            'get_use_case': None,
            'update_use_case': None,
            'delete_use_case': None
        }
