""" Стратегии поиска фильмов """


from telegram.ext import ContextTypes
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from ...base.results import HandlerResult
from ..navigation import BaseCallbackStrategy


class SearchMoviesStrategy(BaseCallbackStrategy):
    """ Стратегия поиска фильмов по жанру """

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
        return callback_data == "search_movies"


class RandomMovieStrategy(BaseCallbackStrategy):
    """ Стратегия случайного фильма """

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
        return callback_data == "random_movie"
