"""Основной обработчик текстового ввода"""

from telegram import Update
from telegram.ext import ContextTypes

from .router import TextRouter
from ..services import (
    MovieService,
    GenreClassificationService,
    RecommendationService
)


class TextHandler:
    """Главный обработчик текстового ввода"""

    def __init__(
        self,
        movie_service: MovieService,
        genre_service: GenreClassificationService,
        recommendation_service: RecommendationService,
    ):
        self._router = TextRouter(
            movie_service=movie_service,
            recommendation_service=recommendation_service,
            genre_service=genre_service,
        )

    async def handle(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Обработать текстовое сообщение"""

        if not update.message or not update.message.text:
            return

        await self._router.route(update, context)
