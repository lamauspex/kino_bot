""" Обработчик команды /start """

import logging

from telegram import Update
from telegram.ext import ContextTypes

from ..base.results import HandlerResult
from ..common.keyboards import get_main_menu_keyboard

logger = logging.getLogger(__name__)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    """ Обработчик команды /start """

    logger.info("Команда /start получена от пользователя: %s",
                update.effective_user.id)

    welcome_text = (
        "🎬 Добро пожаловать в бота для поиска фильмов!\n\n"
        "Я помогу вам:\n"
        "• Найти фильмы по жанру\n"
        "• Получить случайную рекомендацию\n"
        "• Найти похожие фильмы\n"
        "• Узнать подробную информацию о фильме\n\n"
        "Выберите действие в меню ниже:"
    )

    # Отправляем сообщение пользователю
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_menu_keyboard()
    )
