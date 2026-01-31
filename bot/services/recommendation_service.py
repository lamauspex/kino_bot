"""Сервис рекомендаций фильмов"""

import logging
from typing import List, Tuple

from .base import AbstractService
from .movie_service import MovieService
from ..config.recom_config import RecommendationConfig

logger = logging.getLogger(__name__)


class RecommendationService(AbstractService):
    """Сервис рекомендаций фильмов"""

    def __init__(
        self,
        movie_service: MovieService,
        config: RecommendationConfig,
    ):
        self._movie_service = movie_service
        self._config = config
        logger.info("RecommendationService инициализирован")

    async def get_similar_movies(
        self,
        movie_title: str,
        limit: int = 5
    ) -> List[Tuple[str, str]]:
        """Найти похожие фильмы"""

        # Логика поиска похожих фильмов по жанру/описанию
        try:
            movie = await self._movie_service.get_movie_info(movie_title)
            if movie[0] is None:
                return []

            # Упрощённая логика - возвращаем фильмы того же жанра
            genre = movie[0].get('genre', '') if isinstance(
                movie[0], dict) else ''
            similar = await self._movie_service.find_by_genre(genre, limit + 1)

            # Исключаем текущий фильм
            similar = [m for m in similar if m != movie_title]

            return [(m, f"https://example.com/{m}") for m in similar[:limit]]

        except Exception as e:
            logger.error(f"Ошибка поиска похожих: {e}")
            return []

    async def get_by_genre(
        self,
        genre: str,
        limit: int = None
    ) -> List[str]:
        """Найти фильмы по жанру"""

        limit = limit or self._config.NUM_RECOMMENDATIONS
        return await self._movie_service.find_by_genre(genre, limit)
