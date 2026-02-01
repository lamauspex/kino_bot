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
from bot.services.genre_classification_service import GenreClassificationService


class GenrePredictionTextStrategy(AbstractTextStrategy):
    """Стратегия обработки описания для предсказания жанра"""

    def __init__(self, genre_service: GenreClassificationService):
        self._genre_service = genre_service

    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> HandlerResult:
        user_message = update.message.text

        predicted_genre = await self._genre_service.predict(user_message)

        context.user_data['predicted_genre'] = predicted_genre

        keyboard = [
            [InlineKeyboardButton("Да", callback_data='search_movies')],
            [InlineKeyboardButton("В меню", callback_data='main_menu')],
        ]

        return HandlerResult(
            text=f"Это похоже на: {predicted_genre or 'неизвестный жанр'}\n"
            f"Поищем фильмы?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    def matches_state(self, state: Optional[str]) -> bool:
        return state == 'search_genre'
