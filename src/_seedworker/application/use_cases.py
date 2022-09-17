from abc import ABC
import abc
from typing import Generic, TypeVar

Input = TypeVar('Input')
Output = TypeVar('Output')

#pylint: disable=too-few-public-methods


class UseCase(Generic[Input, Output], ABC):
    @abc.abstractmethod
    def execute(self, input_params: Input) -> Output:
        raise NotImplementedError()
