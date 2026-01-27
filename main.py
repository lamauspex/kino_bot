""" Файл запуска """


import asyncio

from bot.app import app


if __name__ == "__main__":
    asyncio.run(app())
