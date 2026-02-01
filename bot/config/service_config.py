
from pydantic import Field

from .base import BaseConfig


class ServiceConfig(BaseConfig):
    """Конфигурация сервисов"""

    # Кэширование
    CACHE_TTL: int = Field(
        description="Время жизни кэша в секундах"
    )
    ENABLE_CACHE: bool = Field(
        description="Включить кэширование"
    )

    # Производительность
    MAX_CONCURRENT_REQUESTS: int = Field(
        description="Макс. одновременных запросов"
    )
    REQUEST_TIMEOUT: int = Field(
        description="Таймаут запроса в секундах"
    )

    # Рекомендации
    DEFAULT_RECOMMENDATION_LIMIT: int = Field(
        description="Лимит рекомендаций по умолчанию"
    )
    SIMILARITY_THRESHOLD: float = Field(
        description="Порог похожести"
    )

    # ML модели
    MODEL_PATH: str = Field(
        description="Путь к моделям"
    )
    ENABLE_ML_RECOMMENDATIONS: bool = Field(
        description="Включить ML рекомендации"
    )

    # Пути к ML моделям
    GENRE_MODEL_PATH: str = Field(
        description="Путь к модели genre"
    )
    VECTORIZER_PATH: str = Field(
        description="Путь к вектору"
    )

    # Параметры поиска
    DEFAULT_SEARCH_LIMIT: int = Field(
        description="Лимит поиска по умолчанию"
    )
    DEFAULT_RECOMMENDATIONS_LIMIT: int = Field(
        description="Лимит рекомендаций по умолчанию"
    )

    # Параметры ML модели
    MODEL_TIMEOUT: int = Field(
        description="Таймаут модели в секундах"
    )
    VECTORIZER_N_FEATURES: int = Field(
        description="Количество признаков в векторе"
    )


service_config = ServiceConfig()
