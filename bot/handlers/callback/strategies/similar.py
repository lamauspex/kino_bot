""" Стратегии для обработки callback queries """


from telegram.ext import ContextTypes
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from bot.handlers.base.results import CallbackAction, HandlerResult
from bot.handlers.callback.strategies.navigation import BaseCallbackStrategy
from bot.services.genre_classification_service import GenreClassificationService
from bot.services.movie_service import MovieService
from bot.services.recommendation_service import RecommendationService


class SimilarMovieStrategy(BaseCallbackStrategy):
    """Стратегия поиска похожих фильмов - установка состояния"""

    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> HandlerResult:
        await update.callback_query.answer()
        context.user_data['state'] = 'similar_movie'

        return HandlerResult(
            text="Напишите название фильма",
            should_stop=True  # Ожидаем текстовый ввод
        )

    def can_handle(self, callback_data: str) -> bool:
        return callback_data == CallbackAction.SIMILAR_MOVIE.value


class TfidfSimilarStrategy(BaseCallbackStrategy):
    """Стратегия поиска похожих фильмов по TF-IDF"""

    def __init__(
        self,
        movie_service: MovieService,
        recommendation_service: RecommendationService,
        genre_service: GenreClassificationService,
        tfidf_service,
    ):
        super().__init__(movie_service, recommendation_service, genre_service)
        self._tfidf_service = tfidf_service

    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> HandlerResult:
        await update.callback_query.answer()

        # Получаем последний запрос пользователя из контекста
        title = context.user_data.get('tfidf_search_title', '')

        if not title:
            return HandlerResult(text="Сначала введите название фильма")

        recommendations = self._tfidf_service.get_recommendations(title)

        if not recommendations:
            # Попробуем найти по частичному совпадению
            similar_titles = self._tfidf_service.find_by_title_contains(title)
            if similar_titles:
                keyboard = [
                    [InlineKeyboardButton(
                        name,
                        callback_data=f'tfidf_select:{name}'
                    ) for name in similar_titles[:2]],
                    [InlineKeyboardButton(
                        "В меню", callback_data='main_menu')],
                ]
                return HandlerResult(
                    text="Выберите фильм:",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            return HandlerResult(text="Похожие фильмы не найдены")

        text = "Похожие фильмы:\n" + "\n".join(
            f"{name} ({url})" for name, url in recommendations
        )

        keyboard = [
            [InlineKeyboardButton(
                "Ещё варианты", callback_data='similar_movie')],
            [InlineKeyboardButton("В меню", callback_data='main_menu')],
        ]

        return HandlerResult(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    def can_handle(self, callback_data: str) -> bool:
        return callback_data == 'tfidf_similar'
