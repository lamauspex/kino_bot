"""Сервис классификации жанров"""


import asyncio
import re
import joblib
from typing import Optional
from bot.config.ml_config import MLConfig
from bot.config.performance_config import PerformanceConfig
from bot.interfaces.interfaces_service import GenreClassificationServiceProtocol


class GenreClassificationService(GenreClassificationServiceProtocol):
    """Сервис классификации жанра по описанию"""

    def __init__(
        self,
        ml_config: MLConfig,
        performance_config: PerformanceConfig
    ):
        self._ml_config = ml_config
        self._performance_config = performance_config
        self._model = None
        self._vectorizer = None
        self._lock = asyncio.Lock()

    async def load_model(self):
        """Ленивая загрузка модели"""

        if self._model is None:

            model_path = self._ml_config.GENRE_MODEL_PATH
            vectorizer_path = self._ml_config.VECTORIZER_PATH

            self._model = joblib.load(model_path)
            self._vectorizer = joblib.load(vectorizer_path)

    async def predict(self, description: str) -> Optional[str]:
        """Предсказать жанр по описанию"""

        try:
            await self.load_model()

            # Предобработка текста
            cleaned = self._preprocess_text(description)

            # Векторизация
            vector = self._vectorizer.transform([cleaned])

            # Предсказание
            predicted = self._model.predict(vector)[0]

            return predicted

        except Exception as e:

            return f"Ошибка классификации: {e}"

    def _preprocess_text(self, text: str) -> str:
        """Предобработка текста"""

        text = text.lower()
        text = re.sub(r'\W+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
