

import asyncio
from typing import Optional

import pandas as pd

from bot.config.data_config import DataConfig
from bot.models.movie import Movie
from .interfaces import MovieRepositoryProtocol


class CachedMovieRepository(MovieRepositoryProtocol):
    """Кэшированный репозиторий фильмов с async/await"""

    def __init__(self, data_config: DataConfig):
        self._data_config = data_config
        self._cache: Optional[pd.DataFrame] = None
        self._cache_lock = asyncio.Lock()

    async def _ensure_cache_loaded(self):
        """Потокобезопасная загрузка кэша"""

        async with self._cache_lock:
            if self._cache is None:
                # Асинхронная загрузка данных
                loop = asyncio.get_event_loop()
                self._cache = await loop.run_in_executor(
                    None,
                    lambda: pd.read_csv(self._data_config.DATA_MOVIES_PATH)
                )

    async def get_by_title(self, title: str) -> Optional[Movie]:
        """Получить фильм по названию"""

        await self._ensure_cache_loaded()

        loop = asyncio.get_event_loop()
        movie_data = await loop.run_in_executor(
            None,
            lambda: self._cache[
                self._cache['title'].str.lower() == title.lower()
            ].iloc[0] if not self._cache.empty else None
        )

        if movie_data is None:
            return None

        return Movie(
            id=str(movie_data.name),
            title=movie_data['title'],
            description=movie_data.get('description', ''),
            genre=movie_data.get('genre', ''),
            director=movie_data.get('director', ''),
            link=movie_data.get('link', '')
        )
