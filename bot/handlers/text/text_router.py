""" Роутер для текстового ввода """

import logging
from typing import List

from telegram import Update
from telegram.ext import ContextTypes

from ..base.base import HandlerResult, AbstractTextStrategy
from ...services.movie_service import MovieService
from ...services.recommendation_service import RecommendationService
from ...services.genre_classification_service import GenreClassificationService

logger = logging.getLogger(__name__)


class TextRouter:
    """ Роутер для маршрутизации текстового ввода """

    def __init__(
        self,
        movie_service: MovieService,
        recommendation_service: RecommendationService,
        genre_service: GenreClassificationService,
    ):
        self._strategies: List[AbstractTextStrategy] = []
        self._movie_service = movie_service
        self._recommendation_service = recommendation_service
        self._genre_service = genre_service
        self._register_default_strategies()

    def _register_default_strategies(self):
        """ Регистрация стандартных стратегий """

        from .strategies.text_strategies import (
            MovieInfoTextStrategy,
            GenrePredictionTextStrategy,
            SimilarMovieTextStrategy,
        )

        self._strategies.append(MovieInfoTextStrategy(self._movie_service))
        self._strategies.append(
            GenrePredictionTextStrategy(self._genre_service)
        )
        self._strategies.append(
            SimilarMovieTextStrategy(self._recommendation_service)
        )

    async def route(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> HandlerResult:
        """ Маршрутизировать текстовый ввод """

        user_message = update.message.text
        current_state = context.user_data.get('state')

        logger.info(
            f"Routing text: {user_message[:50]}... state={current_state}"
        )

        for strategy in self._strategies:
            if strategy.matches_state(current_state):
                result = await strategy.execute(update, context)
                if not result.should_stop:
                    return result

        # Если ни одна стратегия не обработала
        return HandlerResult(should_stop=True)
