
""" Стратегии для обработки текстового ввода """


from typing import Optional

from telegram.ext import ContextTypes
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from bot.handlers.base.abstract import AbstractTextStrategy
from bot.handlers.base.results import HandlerResult
from bot.services.movie_service import MovieService


class MovieInfoTextStrategy(AbstractTextStrategy):
    """Стратегия обработки запроса информации о фильме"""

    def __init__(
        self,
        movie_service: MovieService,
    ):
        self._movie_service = movie_service

    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> HandlerResult:

        user_message = update.message.text

        if not user_message.startswith('Расскажи о фильме'):
            return HandlerResult(should_stop=True)  # Не обрабатывать

        movie_title = user_message[len('Расскажи о фильме'):].strip()

        info_text, _ = await self._movie_service.get_movie_info(movie_title)

        keyboard = [
            [InlineKeyboardButton(
                "В меню",
                callback_data='main_menu'
            )],
        ]

        return HandlerResult(
            text=info_text or "Фильм не найден",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    def matches_state(self, state: Optional[str]) -> bool:
        return True  # Обрабатываем в любом состоянии
