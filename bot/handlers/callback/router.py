""" Роутер для callback стратегий """


from telegram import Update
from telegram.ext import ContextTypes

from ..base.abstract import AbstractStrategy
from ..services import (
    MovieService,
    RecommendationService,
    GenreClassificationService
)
from .strategies.navigation import MainMenuStrategy
from .strategies.search import SearchMoviesStrategy, RandomMovieStrategy
from .strategies.genre import SearchGenreStrategy
from .strategies.similar import SimilarMovieStrategy, TfidfSimilarStrategy
from .strategies.recommendations import GetRecommendationsStrategy


class CallbackRouter:
    """Роутер для callback стратегий"""

    def __init__(
        self,
        movie_service: MovieService,
        recommendation_service: RecommendationService,
        genre_service: GenreClassificationService,
        tfidf_service=None,
    ):
        self._movie_service = movie_service
        self._recommendation_service = recommendation_service
        self._genre_service = genre_service
        self._tfidf_service = tfidf_service
        self._strategies = {}

        self._register_default_strategies()

    def _register_default_strategies(self):
        """ Регистрация стандартных стратегий """

        self.add_strategy("main_menu", MainMenuStrategy(
            self._movie_service,
            self._recommendation_service,
            self._genre_service
        ))

        self.add_strategy("search_movies", SearchMoviesStrategy(
            self._movie_service,
            self._recommendation_service,
            self._genre_service
        ))

        self.add_strategy("random_movie", RandomMovieStrategy(
            self._movie_service,
            self._recommendation_service,
            self._genre_service
        ))

        self.add_strategy("search_genre", SearchGenreStrategy(
            self._movie_service,
            self._recommendation_service,
            self._genre_service
        ))

        self.add_strategy("similar_movie", SimilarMovieStrategy(
            self._movie_service,
            self._recommendation_service,
            self._genre_service
        ))

        self.add_strategy("tfidf_similar", TfidfSimilarStrategy(
            self._movie_service,
            self._recommendation_service,
            self._genre_service,
            self._tfidf_service
        ))

        self.add_strategy("get_recommendations", GetRecommendationsStrategy(
            self._movie_service,
            self._recommendation_service,
            self._genre_service
        ))

    def add_strategy(self, callback_data: str, strategy: AbstractStrategy):
        """ Добавить стратегию """

        self._strategies[callback_data] = strategy

    def register(self, strategy: AbstractStrategy):
        """ Зарегистрировать стратегию (альтернативный метод) """

        # Автоматическое определение callback_data из стратегии
        pass

    async def route(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE) -> None:
        """ Маршрутизировать callback к соответствующей стратегии """

        callback_data = update.callback_query.data

        # Извлекаем основное действие (до двоеточия, если есть)
        action = callback_data.split(':')[0]

        strategy = self._strategies.get(action)
        if not strategy:
            await update.callback_query.answer("Неизвестное действие")
            return

        try:
            result = await strategy.execute(update, context)

            if result.text:
                if update.callback_query.message:
                    await update.callback_query.edit_message_text(
                        result.text,
                        reply_markup=result.reply_markup
                    )
                else:
                    await update.effective_message.reply_text(
                        result.text,
                        reply_markup=result.reply_markup
                    )

            if result.next_handler:
                # Переходим к следующему обработчику
                context.user_data['next_handler'] = result.next_handler

        except Exception as e:
            await update.callback_query.answer(f"Ошибка: {str(e)}")
