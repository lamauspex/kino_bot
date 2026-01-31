""" Приветствие """


from telegram.ext import ContextTypes
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    welcome_message = (
        "Hello! Я твой Kино-бот! Я могу найти фильм, рассказать о нем,"
        "подобрать похожий и не только. Нажимай далее и Я все устрою\n"
        "Также, Ты можешь просто написать 'Расскажи о фильме ...'"
    )

    keyboard = [[InlineKeyboardButton(
        "Далее",
        callback_data='main_menu'
    )]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup
    )
