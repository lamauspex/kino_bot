
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


class SimilarMovieTextStrategy(AbstractTextStrategy):
    """Стратегия поиска похожих фильмов через TF-IDF"""

    def __init__(self, recommendation_service, tfidf_service):
        self._recommendation_service = recommendation_service
        self._tfidf_service = tfidf_service

    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> HandlerResult:
        movie_title = update.message.text

        # Пробуем TF-IDF рекомендации
        recommendations = self._tfidf_service.get_recommendations(movie_title)

        if not recommendations:
            # Фоллбек на жанровые рекомендации
            movie_info = await self._recommendation_service.get_similar_movies(
                movie_title
            )
            recommendations = [
                (name, f"https://example.com/{name}")
                for name in movie_info
            ]

        if not recommendations:
            # Попробуем найти по частичному совпадению
            similar_titles = self._tfidf_service.find_by_title_contains(
                movie_title)

            keyboard = [
                [InlineKeyboardButton("В меню", callback_data='main_menu')],
            ]

            if similar_titles:
                keyboard.insert(0, [
                    InlineKeyboardButton(
                        "Возможно вы имели в виду: " + similar_titles[0],
                        callback_data=f'tfidf_select:{similar_titles[0]}'
                    )
                ])

            return HandlerResult(
                text="Похожие фильмы не найдены. Попробуйте другой фильм.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        text = "Похожие фильмы:\n" + "\n".join(
            f"{name} ({url})" for name, url in recommendations
        )

        keyboard = [
            [InlineKeyboardButton(
                "Ещё варианты", callback_data='search_movies')],
            [InlineKeyboardButton("В меню", callback_data='main_menu')],
        ]

        return HandlerResult(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    def matches_state(self, state: Optional[str]) -> bool:
        return state == 'similar_movie'
