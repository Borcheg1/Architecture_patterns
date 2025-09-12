# stdlib
from abc import ABC, abstractmethod

# project
from src.models.domain_models import Batch


class AbstractRepository(ABC):
    @abstractmethod
    def get(self, reference: str) -> Batch:
        raise NotImplementedError

    @abstractmethod
    def add(self, batch: Batch) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Batch]:
        raise NotImplementedError
