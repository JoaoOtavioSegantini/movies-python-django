from dataclasses import asdict, dataclass
from typing import Callable
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from core.category.application.use_cases import (
    CreateCategoryUseCase,
    ListCategoriesUseCase,
    GetCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase
)


@dataclass(slots=True)
class CategoryResource(APIView):

    create_use_case: Callable[[], CreateCategoryUseCase]
    list_use_case: Callable[[], ListCategoriesUseCase]
    get_use_case: Callable[[], GetCategoryUseCase]
    update_use_case: Callable[[], UpdateCategoryUseCase]
    delete_use_case: Callable[[], DeleteCategoryUseCase]

    def post(self, request: Request):
        input_params = CreateCategoryUseCase.Input(**request.data)
        output = self.create_use_case().execute(input_params)
        return Response(asdict(output), status=HTTP_201_CREATED)

    def get(self, request: Request, id: str = None):  # pylint: disable=invalid-name, redefined-builtin

        if id:
            return self.get_object(id)

        input_params = ListCategoriesUseCase.Input(
            **request.query_params.dict())
        output = self.list_use_case().execute(input_params)
        return Response(asdict(output))

    def get_object(self, id: str):  # pylint: disable=invalid-name, redefined-builtin
        input_params = GetCategoryUseCase.Input(id)
        output = self.get_use_case().execute(input_params)
        return Response(asdict(output))

    def put(self, request: Request, id: str):  # pylint: disable=invalid-name, redefined-builtin
        input_params = UpdateCategoryUseCase.Input(
            **{'id': id, **request.data})
        output = self.update_use_case().execute(input_params)
        return Response(asdict(output))

    def delete(self, request: Request, id: str):  # pylint: disable=invalid-name, redefined-builtin, unused-argument
        input_params = DeleteCategoryUseCase.Input(id)
        self.delete_use_case().execute(input_params)
        return Response(status=HTTP_204_NO_CONTENT)
