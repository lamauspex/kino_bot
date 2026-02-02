"""Конфигурация производительности"""

from pydantic import Field

from .base import BaseConfig


class PerformanceConfig(BaseConfig):
    """Конфигурация производительности"""

    # Основные параметры производительности
    MAX_CONCURRENT_REQUESTS: int = Field(
        default=10,
        description="Макс. одновременных запросов"
    )
    REQUEST_TIMEOUT: int = Field(
        default=30,
        description="Таймаут запроса в секундах"
    )
    MODEL_TIMEOUT: int = Field(
        default=30,
        description="Таймаут модели в секундах"
    )
    VECTORIZER_N_FEATURES: int = Field(
        default=10000,
        description="Количество признаков в векторе"
    )


performance_config = PerformanceConfig()
