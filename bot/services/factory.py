
from typing import TypeVar, Type


from bot.config import data_config
from bot.config.recom_config import RecommendationConfig
from bot.repositories.interfaces import MovieRepositoryProtocol, RecommendationRepositoryProtocol
from bot.repositories.movie_repository import CachedMovieRepository
from bot.repositories.tfidf_recommendation_repository import TfidfRecommendationRepository
from bot.services.interfaces import MovieServiceProtocol, RecommendationServiceProtocol
from bot.services.movie_service import MovieService
from bot.services.recommendation_service import RecommendationService

T = TypeVar('T')


class ServiceFactory:
    """Фабрика сервисов с поддержкой различных реализаций"""

    _services: dict[Type, object] = {}

    @classmethod
    def create_movie_service(
        cls,
        repository_type: Type[MovieRepositoryProtocol] = CachedMovieRepository
    ) -> MovieServiceProtocol:
        """Создать сервис фильмов"""

        if MovieService not in cls._services:
            repository = repository_type(data_config)
            cls._services[MovieService] = MovieService(repository)

        return cls._services[MovieService]

    @classmethod
    def create_recommendation_service(
        cls,
        repository_type: Type[RecommendationRepositoryProtocol] = TfidfRecommendationRepository
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
