"""Конфигурация кэширования"""

from pydantic import Field

from .base import BaseConfig


class CacheConfig(BaseConfig):
    """Конфигурация кэширования"""

    CACHE_TTL: int = Field(
        default=3600,
        description="Время жизни кэша в секундах"
    )
    ENABLE_CACHE: bool = Field(
        default=True,
        description="Включить кэширование"
    )


cache_config = CacheConfig()
