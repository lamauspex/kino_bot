""" Главное меню бота """

from telegram import Update
from telegram.ext import ContextTypes

from ..base.results import HandlerResult
from ..common.keyboards import get_main_menu_keyboard


async def main_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> HandlerResult:
    """ Главное меню """

    context.user_data.clear()  # Очищаем состояние

    return HandlerResult(
        text="🎬 Главное меню\n\nВыберите действие:",
        reply_markup=get_main_menu_keyboard()
    )
