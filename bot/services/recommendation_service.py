
from typing import List

from bot.models.movie import Movie, MovieRecommendation
from bot.repositories.interfaces import (
    MovieRepositoryProtocol,
    RecommendationRepositoryProtocol
)
from bot.config.recom_config import RecommendationConfig
from .interfaces import RecommendationServiceProtocol


class RecommendationService(RecommendationServiceProtocol):
    """Сервис рекомендаций с множественными стратегиями"""

    def __init__(
        self,
        movie_repository: MovieRepositoryProtocol,
        recommendation_repository: RecommendationRepositoryProtocol,
        recommendation_config: RecommendationConfig
    ):
        self._movie_repository = movie_repository
        self._recommendation_repository = recommendation_repository
        self._config = recommendation_config

    async def get_similar_movies(
        self,
        movie_title: str,
        limit: int = 5
    ) -> List[MovieRecommendation]:
        """Получить похожие фильмы"""

        try:
            movie = await self._movie_repository.get_by_title(movie_title)
            if movie is None:
                return []

            return await self._recommendation_repository.get_similar_movies(
                movie, limit
            )

        except Exception as e:
            return f"Ошибка: {e}"

    async def get_by_genre(
        self,
        genre: str,
        limit: int = None
    ) -> List[Movie]:
        """Получить фильмы по жанру"""

        limit = limit or self._config.NUM_RECOMMENDATIONS
        return await self._recommendation_repository.get_by_genre(genre, limit)
