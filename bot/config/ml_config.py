"""Конфигурация ML моделей"""

from pydantic import Field

from .base import BaseConfig


class MLConfig(BaseConfig):
    """Конфигурация ML моделей"""

    MODEL_PATH: str = Field(
        default="./models/",
        description="Путь к моделям"
    )
    ENABLE_ML_RECOMMENDATIONS: bool = Field(
        default=True,
        description="Включить ML рекомендации"
    )
    GENRE_MODEL_PATH: str = Field(
        default="models/genre_model.joblib",
        description="Путь к модели genre"
    )
    VECTORIZER_PATH: str = Field(
        default="models/vectorizer.joblib",
        description="Путь к векторизатору"
    )


ml_config = MLConfig()
