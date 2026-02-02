
""" Конфигурационный файл (токены, URL и прочее) """


from pydantic import Field

from .base import BaseConfig


class BotConfig(BaseConfig):
    """ Конфигурация данных бота """

    TOKEN: str = Field(
        default='',
        description='Ваш токен бота'
    )


bot_config = BotConfig()
