

from .bot_config import bot_config
from .data_config import data_config
from .recom_config import recomm_config


class _SettingsHolder:
    """ Холдер для синглтона """

    instance = None


class SettingsBot:
    """ Центральный объект конфигурации """

    def __new__(cls):
        if _SettingsHolder.instance is None:
            _SettingsHolder.instance = super().__new__(cls)
            _SettingsHolder.instance._initialized = False
        return _SettingsHolder.instance

    def __init__(self):

        # Инициализируем только один раз
        if self._initialized:
            return

        self.bot = bot_config()
        self.crawler = data_config()
        self.recomm = recomm_config()
        self._initialized = True


settings = SettingsBot()
