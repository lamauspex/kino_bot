""" Навигационные стратегии для callback'ов """


from telegram import Update
from telegram.ext import ContextTypes

from ...base.abstract import AbstractStrategy
from ...base.results import HandlerResult
from bot.services import (
    GenreClassificationService,
    MovieService,
    RecommendationService
)


class BaseCallbackStrategy(AbstractStrategy):
    """ Базовая стратегия для callback обработчиков """

    def __init__(
        self,
        movie_service: MovieService,
        recommendation_service: RecommendationService,
        genre_service: GenreClassificationService,
    ):
        self._movie_service = movie_service
        self._recommendation_service = recommendation_service
        self._genre_service = genre_service


class MainMenuStrategy(BaseCallbackStrategy):
    """ Стратегия возврата в главное меню """

    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> HandlerResult:
        await update.callback_query.answer()
        context.user_data.clear()

        return HandlerResult(
            text="🎬 Главное меню",
            next_handler="menu"
        )

    def can_handle(self, callback_data: str) -> bool:
        return callback_data == "main_menu"
