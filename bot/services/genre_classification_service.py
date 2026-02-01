"""Сервис классификации жанров"""


import os
import re
import joblib
from typing import Optional

from .base import AbstractService


class GenreClassificationService(AbstractService):
    """Сервис классификации жанра по описанию"""

    def __init__(self):
        self._model = None
        self._vectorizer = None

    async def load_model(self):
        """Ленивая загрузка модели"""

        if self._model is None:

            model_path = os.path.join(
                '..', '..', 'model_fit', 'genre_model.joblib'
            )
            vectorizer_path = os.path.join(
                '..', '..', 'model_fit', 'vectorizer.joblib'
            )

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
