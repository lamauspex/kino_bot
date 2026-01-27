"""Базовый сервис"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class AbstractRepository(ABC, Generic[T]):
    """Абстрактный репозиторий для работы с данными"""

    @abstractmethod
    def get_all(self) -> T:
        """Получить все данные"""
        pass

    @abstractmethod
    def find_by_id(self, id_value: str):
        """Найти по ID"""
        pass

    @abstractmethod
    def find_by_field(self, field: str, value: str):
        """Найти по полю"""
        pass


class AbstractService(ABC):
    """Базовый класс сервиса"""
    pass
