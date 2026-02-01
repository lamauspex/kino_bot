""" Конфигурационный файл """

from pydantic import Field

from .base import BaseConfig


class RecommendationConfig(BaseConfig):
    """ Конфигурация рекомендаций """

    NUM_RECOMMENDATIONS: int = Field(
        default=5,
        description='Количество рекомендаций'
    )


recommendation_config = RecommendationConfig()
