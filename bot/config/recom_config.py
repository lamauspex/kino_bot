""" Конфигурационный файл """

from pydantic import Field

from .base import BaseConfig


class MoviesRecommendationConfig(BaseConfig):
    """ Конфигурация рекомендаций """

    NUM_RECOMMENDATIONS: int = Field(
        description='Количество рекомендаций'
    )


recomm_config = MoviesRecommendationConfig()
