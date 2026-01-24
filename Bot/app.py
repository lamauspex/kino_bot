""" Сборка приложения """

from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ApplicationBuilder,
    MessageHandler,
    filters
)

from config.bot_config import bot_config
from bot.handlers import start
from bot.handlers.callbacks import button_callback
from bot.handlers.text import handle_user_input
import nest_asyncio


# Создание приложения
app = ApplicationBuilder().token(bot_config.TOKEN).build()

nest_asyncio.apply()


async def app_bot():
    """ Запуск приложения """

    app = ApplicationBuilder().token(bot_config.TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))

    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_user_input,
        block=True
    ))

    print("Бот запущен и готов к работе!")
    await app.run_polling()
