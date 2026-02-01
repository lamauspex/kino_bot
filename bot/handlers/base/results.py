"""Результаты выполнения обработчиков"""


from enum import Enum
from typing import Optional

from telegram import InlineKeyboardMarkup


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
