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
from .handlers import (
    start,
    button_callback,
    handle_user_input
)


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """Фабрика приложения - создаёт и конфигурирует бота"""

    logger.info("Создание приложения...")

    # Инициализация контейнера (опционально - проверить соединения)
    container.config().verify()

    app = ApplicationBuilder().token(
        container.settings().bot.TOKEN
    ).build()

    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_user_input,
        block=True
    ))

    logger.info("Обработчики зарегистрированы")
    return app


async def app_bot():
    """Запуск приложения"""

    app = create_app()

    logger.info("Бот запущен и готов к работе!")
    await app.run_polling()


# Для обратной совместимости - глобальные объекты
app = create_app()
