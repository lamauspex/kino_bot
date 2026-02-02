""" Конфигурация """

from ..config import (
    bot_config,
    data_config,
    cache_config,
    performance_config,
    recommendations_config,
    ml_config
)


class _SettingsHolder:
    """ Холдер для синглтона """

    instance = None


class SettingsBot:
    """
    Центральный объект конфигурации

    Обеспечивает единый доступ ко всем настройкам:
    - bot: Конфигурация бота (токены, API)
    - data: Конфигурация данных (CSV файлы)
    - cache: Конфигурация кэширования
    - performance: Конфигурация производительности
    - recommendations: Конфигурация рекомендаций
    - ml: Конфигурация ML моделей
    """

    def __new__(cls):
        if _SettingsHolder.instance is None:

            _SettingsHolder.instance = super().__new__(cls)
            _SettingsHolder.instance._initialized = False

        return _SettingsHolder.instance

    def __init__(self):

        # Инициализируем только один раз
        if self._initialized:
            return

        self.bot = bot_config
        self.data = data_config
        self.cache = cache_config
        self.performance = performance_config
        self.recommendations = recommendations_config
        self.ml = ml_config

        self._initialized = True


settings = SettingsBot()
