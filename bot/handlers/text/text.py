""" Текстовый ввод - использует Strategy паттерн """


import logging
from telegram import Update
from telegram.ext import ContextTypes

from .text_router import TextRouter

logger = logging.getLogger(__name__)


class TextHandler:
    """ Обработчик текстового ввода с использованием Strategy паттерна """

    def __init__(
        self,
        movie_service,
        genre_service,
        recommendation_service,
    ):
        self._router = TextRouter(
            movie_service,
            recommendation_service,
            genre_service
        )
        logger.info("TextHandler инициализирован")

    async def handle(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        """Обработать текстовый ввод"""

        try:
            result = await self._router.route(update, context)

            if result.text:
                if result.reply_markup:
                    await update.message.reply_text(
                        result.text,
                        reply_markup=result.reply_markup
                    )
                else:
                    await update.message.reply_text(result.text)

        except Exception as e:
            logger.error(f"Ошибка в TextHandler: {e}")
            await update.message.reply_text("Произошла ошибка")


async def handle_user_input(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """ Обёртка для обратной совместимости - использует DI контейнер """

    from bot.containers import container

    handler = container.text_handler()
    await handler.handle(update, context)
