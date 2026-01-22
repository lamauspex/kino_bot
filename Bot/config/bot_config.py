
""" Конфигурационный файл (токены, URL и прочее) """


from pydantic import Field

from bot.config.base import BaseConfig


class BotConfig(BaseConfig):
    """ Конфигурация данных бота """

    TOKEN: str = Field(description='Ваш токен бота')


bot_config = BotConfig()
