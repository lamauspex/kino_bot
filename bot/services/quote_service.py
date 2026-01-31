"""Сервис для работы с цитатами"""

import logging
from typing import Tuple

from .base import AbstractService
from ..config.data_config import DataConfig

logger = logging.getLogger(__name__)


class QuoteRepository:
    """Репозиторий цитат с кэшированием"""

    def __init__(self, data_config: DataConfig):
        self._data_config = data_config
        self._cache = None

    @property
    def dataframe(self):
        if self._cache is None:
            self._cache = self._data_config.DATA_QUOTES
            logger.info("Quotes DataFrame загружен в кэш")
        return self._cache

    def get_random(self) -> Tuple[str, str]:
        """Получить случайную цитату"""

        row = self.dataframe.sample(1).iloc[0]
        return row['phrase'], row['author']


class QuoteService(AbstractService):
    """Сервис цитат"""

    def __init__(self, data_config: DataConfig):
        self._repository = QuoteRepository(data_config)
        logger.info("QuoteService инициализирован")

    async def get_random(self) -> str:
        """Получить случайную цитату"""

        phrase, author = self._repository.get_random()
        return f"...{phrase}...\n{author}"
