"""Абстрактные классы для паттернов Strategy и Command"""

from abc import ABC, abstractmethod
from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes

from .results import HandlerResult


class AbstractStrategy(ABC):
    """Базовый класс для стратегий обработки"""

    @abstractmethod
    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> HandlerResult:
        """Выполнить стратегию"""
        pass

    @abstractmethod
    def can_handle(self, callback_data: str) -> bool:
        """Проверить, может ли стратегия обработать данные"""
        pass


class AbstractCommand(ABC):
    """Базовый класс для команд (текстовый ввод)"""

    @abstractmethod
    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> HandlerResult:
        """Выполнить команду"""
        pass

    @property
    @abstractmethod
    def pattern(self) -> str:
        """Паттерн для распознавания команды"""
        pass


class AbstractTextStrategy(ABC):
    """Стратегия для обработки текстового ввода в определённом состоянии"""

    @abstractmethod
    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> HandlerResult:
        """Выполнить стратегию"""
        pass

    @abstractmethod
    def matches_state(self, state: Optional[str]) -> bool:
        """Проверить соответствие состоянию"""
        pass
