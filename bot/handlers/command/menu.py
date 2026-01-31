
""" Главное меню """


from telegram.ext import ContextTypes
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from ..function import get_random_quote
from ...config import settings


async def main_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    movies_df = settings.data_config.DATA_MOVIES

    quote = get_random_quote(movies_df)
    await update.message.reply_text(quote)

    keyboard = [
        [InlineKeyboardButton(
            "Найти фильм по жанру",
            callback_data='search_genre'
        )],
        [InlineKeyboardButton(
            "Случайный фильм",
            callback_data='random_movie'
        )],
        [InlineKeyboardButton(
            "Подобрать похожий фильм",
            callback_data='similar_movie'
        )],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Выбери действие:",
        reply_markup=reply_markup
    )
