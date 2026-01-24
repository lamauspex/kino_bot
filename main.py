""" Файл запуска """


import asyncio

from bot.app import app_bot


if __name__ == "__main__":
    asyncio.run(app_bot())
