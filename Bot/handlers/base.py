"""Базовые классы для паттернов Strategy и Command"""

from abc import ABC, abstractmethod
from typing import Optional
from enum import Enum

from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes


class HandlerResult:
    """Результат выполнения обработчика"""

    def __init__(
        self,
        text: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        should_stop: bool = False,
        next_handler: Optional[str] = None,
    ):
        self.text = text
        self.reply_markup = reply_markup
        self.should_stop = should_stop
        self.next_handler = next_handler


class CallbackAction(str, Enum):
    """Перечисление всех callback actions"""
    MAIN_MENU = "main_menu"
    SEARCH_MOVIES = "search_movies"
    GET_RECOMMENDATIONS = "get_recommendations"
    RANDOM_MOVIE = "random_movie"
    SEARCH_GENRE = "search_genre"
    SIMILAR_MOVIE = "similar_movie"


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
