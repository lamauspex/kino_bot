"""Репозиторий цитат с кэшированием"""

import asyncio
from typing import Optional
import pandas as pd

from ..config.data_config import DataConfig
from ..models import Quote
from ..interfaces import QuoteRepositoryProtocol


class CachedQuoteRepository(QuoteRepositoryProtocol):
    """Кэшированный репозиторий цитат с async/await"""

    def __init__(self, data_config: DataConfig):
        self._data_config = data_config
        self._cache: Optional[pd.DataFrame] = None
        self._cache_lock = asyncio.Lock()

    @property
    def dataframe(self):
        if self._cache is None:
            self._cache = self._data_config.DATA_QUOTES
        return self._cache

    async def get_random(self) -> Quote:
        """Получить случайную цитату"""

        row = self.dataframe.sample(1).iloc[0]
        return row['phrase'], row['author']
