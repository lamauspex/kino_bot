"""Сервис для работы с фильмами"""

import logging
from typing import Optional, List, Tuple

import pandas as pd

from .base import AbstractService
from ..config.data_config import DataConfig

logger = logging.getLogger(__name__)


class MovieRepository:
    """Репозиторий фильмов с кэшированием"""

    def __init__(self, data_config: DataConfig):
        self._data_config = data_config
        self._cache: Optional[pd.DataFrame] = None

    @property
    def dataframe(self) -> pd.DataFrame:
        """Кэшированный DataFrame"""

        if self._cache is None:
            self._cache = self._data_config.DATA_MOVIES
            logger.info("Movies DataFrame загружен в кэш")
        return self._cache

    def find_by_title(self, title: str) -> Optional[pd.Series]:
        """Найти фильм по названию"""

        matches = self.dataframe[
            self.dataframe['title'].str.lower() == title.lower()
        ]
        return matches.iloc[0] if not matches.empty else None

    def find_by_genre(self, genre: str) -> List[str]:
        """Найти фильмы по жанру"""

        matches = self.dataframe[
            self.dataframe['genre'].str.lower() == genre.lower()
        ]
        return matches['title'].tolist()

    def get_random(self) -> Tuple[str, str, str, str]:
        """Получить случайный фильм"""

        row = self.dataframe.sample(1).iloc[0]
        return (
            row['title'],
            row.get('description', 'Нет описания'),
            row.get('genre', 'Неизвестный жанр'),
            row.get('link', 'Нет ссылки')
        )


class MovieService(AbstractService):
    """Сервис фильмов"""

    def __init__(self, data_config: DataConfig):
        self._repository = MovieRepository(data_config)
        logger.info("MovieService инициализирован")

    async def get_movie_info(
        self,
        movie_title: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """Получить информацию о фильме"""

        try:
            movie = self._repository.find_by_title(movie_title)

            if movie is None:
                return "Фильм не найден", None

            info_text = (
                f"\n{movie['title']}"
                f"\n{movie['genre']}"
                f"\n{movie['director']}"
                f"\n{movie['link']}"
                f"\n{movie['description']}\n"
            )

            return info_text, "main_menu"

        except Exception as e:
            logger.error(f"Ошибка при получении фильма: {e}")
            return "Произошла ошибка при поиске фильма", None

    async def get_random_movie(self) -> Tuple[str, str, str, str]:
        """Получить случайный фильм"""

        return self._repository.get_random()

    async def find_by_genre(
        self,
        genre: str,
        limit: int = 5
    ) -> List[str]:
        """Найти фильмы по жанру"""

        all_movies = self._repository.find_by_genre(genre)
        import random
        return random.sample(
            all_movies,
            min(limit, len(all_movies))
        )
