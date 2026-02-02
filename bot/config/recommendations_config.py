"""Конфигурация рекомендаций"""

from pydantic import Field

from .base import BaseConfig


class RecommendationsConfig(BaseConfig):
    """Конфигурация рекомендаций"""

    NUM_RECOMMENDATIONS: int = Field(
        default=5,
        description="Количество рекомендаций"
    )
    SIMILARITY_THRESHOLD: float = Field(
        default=0.1,
        description="Порог похожести"
    )
    DEFAULT_SEARCH_LIMIT: int = Field(
        default=5,
        description="Лимит поиска по умолчанию"
    )
    DEFAULT_RECOMMENDATIONS_LIMIT: int = Field(
        default=5,
        description="Лимит рекомендаций по умолчанию"
    )


recommendations_config = RecommendationsConfig()
