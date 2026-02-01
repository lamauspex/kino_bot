"""Роутер для текстовых стратегий"""

from telegram import Update
from telegram.ext import ContextTypes

from ..services import MovieService, RecommendationService, GenreClassificationService
from .strategies.movie_info import MovieInfoTextStrategy
from .strategies.genre_prediction import GenrePredictionTextStrategy
from .strategies.similar_movies import SimilarMovieTextStrategy


class TextRouter:
    """Роутер для текстовых стратегий"""

    def __init__(
        self,
        movie_service: MovieService,
        recommendation_service: RecommendationService,
        genre_service: GenreClassificationService,
    ):
        self._movie_service = movie_service
        self._recommendation_service = recommendation_service
        self._genre_service = genre_service
        self._strategies = []

        self._register_default_strategies()

    def _register_default_strategies(self):
        """Регистрация стандартных стратегий"""
        self._strategies = [
            MovieInfoTextStrategy(self._movie_service),
            GenrePredictionTextStrategy(self._genre_service),
            # TODO: добавить tfidf_service
            SimilarMovieTextStrategy(self._recommendation_service, None),
        ]

    async def route(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """Маршрутизировать текст к соответствующей стратегии"""

        current_state = context.user_data.get('state')

        for strategy in self._strategies:
            if strategy.matches_state(current_state):
                try:
                    result = await strategy.execute(update, context)

                    if result.text:
                        await update.message.reply_text(
                            result.text,
                            reply_markup=result.reply_markup
                        )

                    # Обновляем состояние
                    if hasattr(result, 'new_state'):
                        context.user_data['state'] = result.new_state

                    if result.should_stop:
                        break

                except Exception as e:
                    await update.message.reply_text(f"Ошибка: {str(e)}")
                break
