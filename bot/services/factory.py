
from typing import TypeVar, Type

from ..config import (
    data_config,
    RecommendationConfig,
    ServiceConfig
)
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
from ..services import (
    MovieService,
    RecommendationService
)


T = TypeVar('T')


class ServiceFactory:
    """Фабрика сервисов с поддержкой различных реализаций"""

    _services: dict[Type, object] = {}

    @classmethod
    def create_movie_service(
        cls,
        repository_type: Type[MovieRepositoryProtocol] = CachedMovieRepository,
        service_config: ServiceConfig = None
    ) -> MovieServiceProtocol:
        """Создать сервис фильмов"""

        service_config = service_config or ServiceConfig()

        if MovieService not in cls._services:
            repository = repository_type(data_config)
            cls._services[MovieService] = MovieService(repository)

        return MovieService(repository, service_config)

    @classmethod
    def create_recommendation_service(
        cls,
        repository_type: Type[RecommendationRepositoryProtocol] =
            TfidfRecommendationRepository
    ) -> RecommendationServiceProtocol:
        """Создать сервис рекомендаций"""

        if RecommendationService not in cls._services:
            movie_service = cls.create_movie_service()
            repository = repository_type(movie_service._movie_repository)
            config = RecommendationConfig()
            cls._services[RecommendationService] = RecommendationService(
                movie_service._movie_repository, repository, config
            )

        return cls._services[RecommendationService]
