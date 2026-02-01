""" TF-IDF репозиторий рекомендаций """

from typing import List

from bot.models.movie import Movie, MovieRecommendation
from bot.repositories.interfaces import RecommendationRepositoryProtocol


class TfidfRecommendationRepository(RecommendationRepositoryProtocol):
    """Реализация репозитория рекомендаций на основе TF-IDF"""

    def __init__(self, movie_repository):
        """Инициализация с зависимостью от репозитория фильмов"""
        self._movie_repository = movie_repository

    async def get_similar_movies(
        self,
        movie: Movie,
        limit: int = 5
    ) -> List[MovieRecommendation]:
        """Получить похожие фильмы на основе TF-IDF"""
        
        # TODO: Реализовать TF-IDF алгоритм
        # Пока возвращаем пустой список как заглушку
        return []

    async def get_by_genre(
        self,
        genre: str,
        limit: int = 5
    ) -> List[Movie]:
        """Получить фильмы по жанру"""
        
        # Используем существующий метод репозитория фильмов
        return await self._movie_repository.search_by_genre(genre, limit)