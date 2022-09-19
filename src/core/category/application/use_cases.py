

from dataclasses import asdict, dataclass
from typing import Optional

from core.category.domain.entities import Category
from core.category.domain.repositories import CategoryRepository
from core.category.application.dto import CategoryOutputMapper, CategoryOutput
from core._seedworker.application.use_cases import UseCase
from core._seedworker.application.dto import PaginationOutputMapper, SearchInput, PaginationOutput


@dataclass(frozen=True, slots=True)
class CreateCategoryUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, input_params: 'Input') -> 'Output':
        category = Category(
            name=input_params.name,
            description=input_params.description,
            is_active=input_params.is_active
        )

        self.category_repo.insert(category)

        return self.__to_output(category)

    def __to_output(self, category: Category):
        return CategoryOutputMapper\
            .from_child(CreateCategoryUseCase.Output)\
            .to_output(category)

    @dataclass(slots=True, frozen=True)
    class Input:
        name: str
        description: Optional[str] = Category.get_field('description').default
        is_active: Optional[bool] = Category.get_field('is_active').default

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(frozen=True, slots=True)
class GetCategoryUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, input_params: 'Input') -> 'Output':
        category = self.category_repo.find_by_id(input_params.id)

        return self.__to_output(category)

    def __to_output(self, category: Category):
        return CategoryOutputMapper.from_child(GetCategoryUseCase.Output).to_output(category)

    @dataclass(slots=True, frozen=True)
    class Input:
        #pylint: disable=invalid-name
        id: str

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class ListCategoriesUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, input_params: 'Input') -> 'Output':
        search_params = self.category_repo.SearchParams(**asdict(input_params))
        result = self.category_repo.search(search_params)
        return self.__to_output(result)

    def __to_output(self, result: CategoryRepository.SearchResult):
        items = list(
            map(CategoryOutputMapper.without_child().to_output, result.items)
        )
        return PaginationOutputMapper\
            .from_child(ListCategoriesUseCase.Output)\
            .to_output(
                items,
                result
            )

    @dataclass(slots=True, frozen=True)
    class Input(SearchInput[str]):
        pass

    @dataclass(slots=True, frozen=True)
    class Output(PaginationOutput[CategoryOutput]):
        pass


@dataclass(slots=True, frozen=True)
class UpdateCategoryUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, input_params: 'Input') -> 'Output':
        entity = self.category_repo.find_by_id(input_params.id)
        entity.update(input_params.name, input_params.description)

        if input_params.is_active is True:
            entity.activate()

        if input_params.is_active is False:
            entity.deactivate()

        self.category_repo.update(entity)
        return self.__to_output(entity)

    def __to_output(self, category: Category) -> 'Output':
        return CategoryOutputMapper\
            .from_child(UpdateCategoryUseCase.Output)\
            .to_output(category)

    @dataclass(slots=True, frozen=True)
    class Input:
        id: str  # pylint: disable=invalid-name
        name: str
        description: Optional[str] = Category.get_field(
            'description').default
        is_active: Optional[bool] = Category.get_field('is_active').default

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class DeleteCategoryUseCase(UseCase):

    category_repo: CategoryRepository

    def execute(self, input_params: 'Input') -> None:
        self.category_repo.delete(input_params.id)

    @dataclass(slots=True, frozen=True)
    class Input:
        id: str  # pylint: disable=invalid-name
