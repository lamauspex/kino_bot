
# Конфигурационный файл (токены, URL и прочее)

import logging
from telegram import Bot
from telegram.ext import ApplicationBuilder

# Токен вашего бота
TOKEN = 'TOKEN'

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


# Создание приложения
app = ApplicationBuilder().token(TOKEN).build()

