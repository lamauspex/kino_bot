
from typing import List

from ..models import (
    Movie,
    MovieRecommendation
)
from ..interfaces import (
    MovieRepositoryProtocol,
    RecommendationRepositoryProtocol,
    RecommendationServiceProtocol
)
from ..config.recommendations_config import RecommendationsConfig


class RecommendationService(RecommendationServiceProtocol):
    """Сервис рекомендаций с множественными стратегиями"""

    def __init__(
        self,
        movie_repository: MovieRepositoryProtocol,
        recommendation_repository: RecommendationRepositoryProtocol,
        recommendations_config: RecommendationsConfig
    ):
        self._movie_repository = movie_repository
        self._recommendation_repository = recommendation_repository
        self._config = recommendations_config

    async def get_similar_movies(
        self,
        movie_title: str,
        limit: int = None
    ) -> List[MovieRecommendation]:
        """Получить похожие фильмы"""

        limit = limit or self._config.NUM_RECOMMENDATIONS

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
