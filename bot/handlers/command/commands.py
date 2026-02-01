""" Общие команды бота """

from telegram import Update
from telegram.ext import ContextTypes

from ..base import HandlerResult


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> HandlerResult:
    """ Команда помощи """

    help_text = (
        "🤖 Команды бота:\n\n"
        "/start - Начать работу\n"
        "/menu - Главное меню\n"
        "/help - Помощь\n\n"
        "💡 Для поиска фильмов используйте меню или опишите сюжет!"
    )

    return HandlerResult(text=help_text)


async def unknown_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> HandlerResult:
    """ Обработчик неизвестных команд """

    return HandlerResult(
        text="❓ Неизвестная команда. Используйте /help для справки."
    )
