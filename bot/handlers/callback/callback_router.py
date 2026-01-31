"""Роутер для callback queries - заменяет if-elif цепочки"""

import logging
from typing import Dict

from telegram import Update
from telegram.ext import ContextTypes

from ..base.base import AbstractStrategy, HandlerResult
from ...services.movie_service import MovieService
from ...services.recommendation_service import RecommendationService
from ...services.genre_classification_service import GenreClassificationService

logger = logging.getLogger(__name__)


class CallbackRouter:
    """Роутер для маршрутизации callback queries"""

    def __init__(
        self,
        movie_service: MovieService,
        recommendation_service: RecommendationService,
        genre_service: GenreClassificationService,
        tfidf_service=None,
    ):
        self._strategies: Dict[str, AbstractStrategy] = {}
        self._movie_service = movie_service
        self._recommendation_service = recommendation_service
        self._genre_service = genre_service
        self._tfidf_service = tfidf_service
        self._register_default_strategies()

    def _register_default_strategies(self):
        """Регистрация стандартных стратегий"""
        from .callback_strategies import (
            MainMenuStrategy,
            SearchMoviesStrategy,
            RandomMovieStrategy,
            SearchGenreStrategy,
            SimilarMovieStrategy,
            GetRecommendationsStrategy,
            TfidfSimilarStrategy,
        )

        self.register(MainMenuStrategy(
            self._movie_service,
            self._recommendation_service,
            self._genre_service
        ))

        self.register(SearchMoviesStrategy(
            self._movie_service,
            self._recommendation_service,
            self._genre_service
        ))

        self.register(RandomMovieStrategy(
            self._movie_service,
            self._recommendation_service,
            self._genre_service
        ))

        self.register(SearchGenreStrategy(
            self._movie_service,
            self._recommendation_service,
            self._genre_service
        ))

        self.register(SimilarMovieStrategy(
            self._movie_service,
            self._recommendation_service,
            self._genre_service
        ))

        self.register(GetRecommendationsStrategy(
            self._movie_service,
            self._recommendation_service,
            self._genre_service
        ))

        # TF-IDF стратегия
        if self._tfidf_service:
            self.register(TfidfSimilarStrategy(
                self._movie_service,
                self._recommendation_service,
                self._genre_service,
                self._tfidf_service
            ))

    def register(self, strategy: AbstractStrategy) -> None:
        """Зарегистрировать стратегию"""

        self._strategies[strategy.__class__.__name__] = strategy
        logger.debug(
            f"Зарегистрирована стратегия: {strategy.__class__.__name__}")

    async def route(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> HandlerResult:
        """Маршрутизировать callback"""

        callback_data = update.callback_query.data
        logger.info(f"Routing callback: {callback_data}")

        for strategy in self._strategies.values():
            if strategy.can_handle(callback_data):
                return await strategy.execute(update, context)

        logger.warning(f"Не найдена стратегия для: {callback_data}")
        return HandlerResult(text="Неизвестная команда")

    def add_strategy(self, callback_data: str, strategy: AbstractStrategy):
        """Добавить стратегию для конкретного callback_data"""
        self._strategies[callback_data] = strategy
