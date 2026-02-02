
""" Конфигурационный файл (токены, URL и прочее) """


from pydantic import Field

from .base import BaseConfig


class BotConfig(BaseConfig):
    """ Конфигурация данных бота """

    TOKEN: str = Field(
        default='8352703188:AAG7GbqFB3SUBrFHVg0nUtr1BMNev0cdWTM',
        description='Ваш токен бота'
    )


bot_config = BotConfig()
