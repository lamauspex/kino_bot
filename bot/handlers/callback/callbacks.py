""" Обработчик inline кнопок - использует Strategy паттерн """


import logging
from telegram import Update
from telegram.ext import ContextTypes

from .callback_router import CallbackRouter


logger = logging.getLogger(__name__)


class CallbackHandler:
    """Обработчик callback queries с использованием Strategy паттерна"""

    def __init__(
        self,
        movie_service,
        recommendation_service,
        genre_service,
        tfidf_service=None,
    ):
        self._router = CallbackRouter(
            movie_service,
            recommendation_service,
            genre_service,
            tfidf_service
        )
        logger.info("CallbackHandler инициализирован")

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработать callback query"""

        try:
            result = await self._router.route(update, context)

            if result.next_handler == "menu":
                # Перенаправляем в меню
                from ..command.menu import MenuHandler
                menu = MenuHandler(
                    quote_service=None,
                    movie_service=None
                )
                await menu.main_menu(update, context)
                return

            if result.text:
                if update.callback_query.message:
                    try:
                        await update.callback_query.message.edit_text(
                            result.text,
                            reply_markup=result.reply_markup
                        )
                    except Exception:
                        await update.callback_query.message.reply_text(
                            result.text,
                            reply_markup=result.reply_markup
                        )

        except Exception as e:
            logger.error(f"Ошибка в CallbackHandler: {e}")
            await update.callback_query.message.reply_text(
                "Произошла ошибка"
            )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обёртка для обратной совместимости - использует DI контейнер"""

    from bot.containers import container

    handler = container.callback_handler()
    await handler.handle(update, context)
