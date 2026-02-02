"""Сборка приложения - с использованием Dependency Injection"""


import logging

from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ApplicationBuilder,
    MessageHandler,
    filters
)

from .containers import container
from .handlers.command.start import start


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """Фабрика приложения - создаёт и конфигурирует бота"""

    logger.info("Создание приложения...")

    # Инициализация контейнера зависимостей
    container.init_resources()
    logger.info("Контейнер инициализирован")

    # Создаем и конфигурируем приложение
    app = ApplicationBuilder().token(
        container.bot_config().TOKEN
    ).build()
    logger.info("Приложение создано")

    # Создаем обработчики из контейнера
    callback_handler = container.callback_handler()
    text_handler = container.text_handler()
    logger.info("Обработчики созданы")

    # Wrapper функции для обработчиков
    async def button_callback(update, context):
        return await callback_handler.handle(update, context)

    async def handle_user_input(update, context):
        return await text_handler.handle(update, context)

    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", start))
    logger.info("Обработчик /start зарегистрирован")

    app.add_handler(CallbackQueryHandler(button_callback))
    logger.info("Обработчик callback зарегистрирован")

    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_user_input,
        block=True
    ))
    logger.info("Обработчик текста зарегистрирован")

    logger.info("Все обработчики зарегистрированы")
    return app
