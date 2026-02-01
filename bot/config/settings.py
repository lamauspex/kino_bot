""" Конфигурация """


from ..config import (
    bot_config,
    data_config,
    recomm_config,
    service_config
)


class _SettingsHolder:
    """ Холдер для синглтона """

    instance = None


class SettingsBot:
    """
    Центральный объект конфигурации

    Обеспечивает единый доступ ко всем настройкам:
    - bot: Конфигурация бота (токены, API)
    - crawler: Конфигурация данных (CSV файлы)
    - recomm: Конфигурация рекомендаций
    - service: Конфигурация сервисов (ML модели, кэш)
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

        self.bot = bot_config()
        self.crawler = data_config()
        self.recomm = recomm_config()
        self.service = service_config()
        self._initialized = True


settings = SettingsBot()
