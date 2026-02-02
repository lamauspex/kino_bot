from typing import TypeVar, Type

from ..config import settings
from ..repositories import (
    TfidfRecommendationRepository,
    CachedMovieRepository
)
from ..interfaces import (
    MovieRepositoryProtocol,
    RecommendationRepositoryProtocol,
    MovieServiceProtocol,
    RecommendationServiceProtocol
)


T = TypeVar('T')


class ServiceFactory:
    """Фабрика сервисов с поддержкой различных реализаций"""

    _services: dict[Type, object] = {}

    @classmethod
    def create_movie_service(
        cls,
        repository_type: Type[MovieRepositoryProtocol] = CachedMovieRepository,
        service_config=None
    ) -> MovieServiceProtocol:
        """Создать сервис фильмов"""

        service_config = service_config or settings.performance

        if MovieServiceProtocol not in cls._services:
            repository = repository_type(settings.data)
            # Отложенный импорт для избежания циклической зависимости
            from ..services import MovieService
            cls._services[MovieServiceProtocol] = MovieService(
                repository, service_config)

        return cls._services[MovieServiceProtocol]

    @classmethod
    def create_recommendation_service(
        cls,
        repository_type: Type[RecommendationRepositoryProtocol] =
            TfidfRecommendationRepository
    ) -> RecommendationServiceProtocol:
        """Создать сервис рекомендаций"""

        if RecommendationServiceProtocol not in cls._services:
            movie_service = cls.create_movie_service()
            repository = repository_type(movie_service._movie_repository)
            config = settings.recommendations

            # Отложенный импорт для избежания циклической зависимости
            from ..services import RecommendationService
            cls._services[RecommendationServiceProtocol] = \
                RecommendationService(
                movie_service._movie_repository,
                repository, config
            )

        return cls._services[RecommendationServiceProtocol]
