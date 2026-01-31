"""Основной обработчик callback'ов"""

from telegram import Update
from telegram.ext import ContextTypes

from ..base.results import HandlerResult
from .router import CallbackRouter
from ..services import (
    MovieService,
    RecommendationService,
    GenreClassificationService
)


class CallbackHandler:
    """Главный обработчик callback queries"""

    def __init__(
        self,
        movie_service: MovieService,
        recommendation_service: RecommendationService,
        genre_service: GenreClassificationService,
        tfidf_service=None,
    ):
        self._router = CallbackRouter(
            movie_service=movie_service,
            recommendation_service=recommendation_service,
            genre_service=genre_service,
            tfidf_service=tfidf_service,
        )

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработать callback query"""
        if not update.callback_query:
            return

        await self._router.route(update, context)
