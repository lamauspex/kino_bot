

import asyncio
from typing import Optional

import pandas as pd

from ..config import settings
from ..models import Movie
from ..interfaces import MovieRepositoryProtocol


class CachedMovieRepository(MovieRepositoryProtocol):
    """Кэшированный репозиторий фильмов с async/await"""

    def __init__(self, data_config: settings.data_config):
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
        try:
            movie_data = await loop.run_in_executor(
                None,
                lambda: self._cache[
                    self._cache['title'].str.lower() == title.lower()
                ].iloc[0]
            )
            return self._movie_from_row(
                movie_data,
                str(movie_data.name)
            )
        except (IndexError, KeyError):
            return None

    async def get_by_id(self, movie_id: str) -> Optional[Movie]:
        """Получить фильм по ID"""
        await self._ensure_cache_loaded()
        loop = asyncio.get_event_loop()
        try:
            movie_data = await loop.run_in_executor(
                None,
                lambda: self._cache.loc[movie_id]
            )
            return self._movie_from_row(movie_data, movie_id)
        except KeyError:
            return None

    async def get_random(self) -> Movie:
        """Получить случайный фильм"""
        await self._ensure_cache_loaded()
        loop = asyncio.get_event_loop()
        movie_data = await loop.run_in_executor(
            None,
            lambda: self._cache.sample(1).iloc[0]
        )
        return self._movie_from_row(movie_data, str(movie_data.name))

    async def search_by_genre(self, genre: str, limit: int = 10) -> List[Movie]:
        """Поиск фильмов по жанру"""

        await self._ensure_cache_loaded()
        loop = asyncio.get_event_loop()
        movies_data = await loop.run_in_executor(
            None,
            lambda: self._cache[
                self._cache['genre'].str.contains(genre, case=False, na=False)
            ].head(limit)
        )
        return [
            self._movie_from_row(row, str(row.name))
            for _, row in movies_data.iterrows()
        ]

    async def search_by_title_contains(self, query: str, limit: int = 10) -> List[Movie]:
        """Поиск фильмов по названию (частичное совпадение)"""

        await self._ensure_cache_loaded()
        loop = asyncio.get_event_loop()
        movies_data = await loop.run_in_executor(
            None,
            lambda: self._cache[
                self._cache['title'].str.contains(query, case=False, na=False)
            ].head(limit)
        )
        return [
            self._movie_from_row(row, str(row.name))
            for _, row in movies_data.iterrows()
        ]

    def _movie_from_row(self, row, movie_id: str) -> Movie:
        """Вспомогательный метод для создания Movie из DataFrame row"""

        return Movie(
            id=movie_id,
            title=row['title'],
            description=row.get('description', ''),
            genre=row.get('genre', ''),
            director=row.get('director', ''),
            year=row.get('year'),
            rating=row.get('rating'),
            link=row.get('link', '')
        )
