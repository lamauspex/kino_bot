""" Стратегии для обработки callback queries """


import logging

from telegram.ext import ContextTypes
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from .base import (
    AbstractStrategy,
    HandlerResult,
    CallbackAction
)
from ..services import (
    MovieService,
    RecommendationService,
    GenreClassificationService
)


logger = logging.getLogger(__name__)


class BaseCallbackStrategy(AbstractStrategy):
    """Базовая стратегия для callback обработчиков"""

    def __init__(
        self,
        movie_service: MovieService,
        recommendation_service: RecommendationService,
        genre_service: GenreClassificationService,
    ):
        self._movie_service = movie_service
        self._recommendation_service = recommendation_service
        self._genre_service = genre_service

    def can_handle(self, callback_data: str) -> bool:
        """Переопределяется в наследниках"""
        raise NotImplementedError


class MainMenuStrategy(BaseCallbackStrategy):
    """Стратегия возврата в главное меню"""

    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> HandlerResult:
        await update.callback_query.answer()
        context.user_data.clear()

        return HandlerResult(
            text="Главное меню",
            next_handler="menu"
        )

    def can_handle(self, callback_data: str) -> bool:
        return callback_data == CallbackAction.MAIN_MENU.value


class SearchMoviesStrategy(BaseCallbackStrategy):
    """Стратегия поиска фильмов по жанру"""

    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> HandlerResult:
        await update.callback_query.answer()

        predicted_genre = context.user_data.get('predicted_genre')
        if not predicted_genre:
            return HandlerResult(
                text="Сначала опишите сюжет"
            )

        recommendations = await self._recommendation_service.get_by_genre(
            predicted_genre
        )

        if not recommendations:
            return HandlerResult(
                text="Фильмы не найдены"
            )

        recommendations_text = "\n".join(recommendations)

        keyboard = [
            [InlineKeyboardButton(
                "Ещё варианты", callback_data='search_movies')],
            [InlineKeyboardButton("В меню", callback_data='main_menu')],
        ]

        return HandlerResult(
            text=f"Вот что я нашёл:\n{recommendations_text}\n"
            f"Напишите 'Расскажи о ...' для подробностей",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    def can_handle(self, callback_data: str) -> bool:
        return callback_data == CallbackAction.SEARCH_MOVIES.value


class RandomMovieStrategy(BaseCallbackStrategy):
    """Стратегия случайного фильма"""

    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> HandlerResult:
        await update.callback_query.answer()

        title, desc, genre, link = await self._movie_service.get_random_movie()

        text = (
            f"Случайный фильм: {title}\n"
            f"Жанр: {genre}\n"
            f"Описание: {desc}\n"
            f"Ссылка: {link}"
        )

        keyboard = [
            [InlineKeyboardButton("Ещё", callback_data='random_movie')],
            [InlineKeyboardButton("В меню", callback_data='main_menu')],
        ]

        await update.callback_query.edit_message_text(text)

        return HandlerResult(
            text="Что делаем дальше?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    def can_handle(self, callback_data: str) -> bool:
        return callback_data == CallbackAction.RANDOM_MOVIE.value


class SearchGenreStrategy(BaseCallbackStrategy):
    """Стратегия поиска по жанру - установка состояния"""

    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> HandlerResult:
        await update.callback_query.answer()
        context.user_data['state'] = 'search_genre'

        return HandlerResult(
            text="Опишите сюжет фильма",
            should_stop=True  # Ожидаем текстовый ввод
        )

    def can_handle(self, callback_data: str) -> bool:
        return callback_data == CallbackAction.SEARCH_GENRE.value


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


class GetRecommendationsStrategy(BaseCallbackStrategy):
    """Стратегия получения рекомендаций"""

    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> HandlerResult:
        await update.callback_query.answer()

        # Логика получения рекомендаций
        recommendations = await self._recommendation_service.get_similar_movies(
            context.user_data.get('last_movie', ''),
            limit=5
        )

        if not recommendations:
            return HandlerResult(text="Не удалось найти рекомендации")

        text = "Похожие фильмы:\n" + "\n".join(
            f"{name} ({url})" for name, url in recommendations
        )

        keyboard = [
            [InlineKeyboardButton("Ещё", callback_data='get_recommendations')],
            [InlineKeyboardButton("В меню", callback_data='main_menu')],
        ]

        return HandlerResult(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    def can_handle(self, callback_data: str) -> bool:
        return callback_data == CallbackAction.GET_RECOMMENDATIONS.value
