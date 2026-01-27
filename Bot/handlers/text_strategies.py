""" Стратегии для обработки текстового ввода """


import logging
from typing import Optional

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import ContextTypes

from .base import HandlerResult, AbstractTextStrategy
from ..services import MovieService, GenreClassificationService


logger = logging.getLogger(__name__)


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
        logger.info(f"Запрос информации о фильме: {movie_title}")

        info_text, _ = await self._movie_service.get_movie_info(movie_title)

        keyboard = [
            [InlineKeyboardButton("В меню", callback_data='main_menu')],
        ]

        return HandlerResult(
            text=info_text or "Фильм не найден",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    def matches_state(self, state: Optional[str]) -> bool:
        return True  # Обрабатываем в любом состоянии


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

        logger.info(f"Предсказание жанра для: {user_message[:50]}...")
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
        logger.info(f"TF-IDD поиск похожих для: {movie_title}")

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
