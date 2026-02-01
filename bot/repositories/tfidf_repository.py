""" TF-IDF репозиторий рекомендаций """

from typing import List

from ..models import Movie, MovieRecommendation
from ..interfaces import RecommendationRepositoryProtocol


class TfidfRecommendationRepository(RecommendationRepositoryProtocol):
    """Реализация репозитория рекомендаций на основе TF-IDF"""

    def __init__(self, movie_repository):
        """Инициализация с зависимостью от репозитория фильмов"""
        self._movie_repository = movie_repository

    async def get_similar_movies(
        self,
        movie: Movie,
        limit: int = None
    ) -> List[MovieRecommendation]:
        """Получить похожие фильмы на основе TF-IDF"""

        limit = limit or self._config.NUM_RECOMMENDATIONS
        # TODO: Реализовать TF-IDF алгоритм
        # Пока возвращаем пустой список как заглушку
        return []

    async def get_by_genre(
        self,
        genre: str,
        limit: int = None
    ) -> List[Movie]:
        """Получить фильмы по жанру"""

        limit = limit or self._config.NUM_RECOMMENDATIONS
        # Используем существующий метод репозитория фильмов
        return await self._movie_repository.search_by_genre(genre, limit)
