
""" Главное меню """


from telegram.ext import ContextTypes
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from bot.Function.Random_Quote import get_random_quote


async def main_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    quote = get_random_quote(dk)
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
