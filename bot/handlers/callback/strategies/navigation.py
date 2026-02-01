""" Навигационные стратегии для callback'ов """


from telegram import Update
from telegram.ext import ContextTypes

from ...base.abstract import AbstractStrategy
from ...base.results import HandlerResult
from bot.services.genre_classification_service import GenreClassificationService
from bot.services.movie_service import MovieService
from bot.services.recommendation_service import RecommendationService


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
