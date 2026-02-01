
from pydantic import Field

from .base import BaseConfig


class ServiceConfig(BaseConfig):
    """Конфигурация сервисов"""

    # Кэширование
    CACHE_TTL: int = Field(
        default=3600, description="Время жизни кэша в секундах")
    ENABLE_CACHE: bool = Field(
        default=True, description="Включить кэширование")

    # Производительность
    MAX_CONCURRENT_REQUESTS: int = Field(
        default=10, description="Макс. одновременных запросов")
    REQUEST_TIMEOUT: int = Field(
        default=30, description="Таймаут запроса в секундах")

    # Рекомендации
    DEFAULT_RECOMMENDATION_LIMIT: int = Field(
        default=5, description="Лимит рекомендаций по умолчанию")
    SIMILARITY_THRESHOLD: float = Field(
        default=0.1, description="Порог похожести")

    # ML модели
    MODEL_PATH: str = Field(default="./models/", description="Путь к моделям")
    ENABLE_ML_RECOMMENDATIONS: bool = Field(
        default=True, description="Включить ML рекомендации")


service_config = ServiceConfig()
