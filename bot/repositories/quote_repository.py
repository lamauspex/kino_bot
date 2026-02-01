
"""Репозиторий цитат с кэшированием"""


from typing import Tuple

from bot.repositories.interfaces import QuoteRepositoryProtocol
from ..config.data_config import DataConfig


class CachedQuoteRepository(QuoteRepositoryProtocol):

    def __init__(self, data_config: DataConfig):
        self._data_config = data_config
        self._cache = None

    @property
    def dataframe(self):
        if self._cache is None:
            self._cache = self._data_config.DATA_QUOTES
        return self._cache

    def get_random(self) -> Tuple[str, str]:
        """Получить случайную цитату"""

        row = self.dataframe.sample(1).iloc[0]
        return row['phrase'], row['author']
