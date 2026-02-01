
from bot.config.base import BaseConfig
from bot.config.data_config import DataConfig
from bot.config.recom_config import RecommendationConfig
from dependency_injector import containers, providers

from bot.repositories.interfaces import *
from bot.repositories.tfidf_recommendation_repository import TfidfRecommendationRepository
from bot.services.interfaces import *
from bot.repositories.movie_repository import CachedMovieRepository
from bot.services.movie_service import MovieService
from bot.services.recommendation_service import RecommendationService
from bot.services.genre_classification_service import GenreClassificationService
from bot.services.quote_service import QuoteService


class EnhancedContainer(containers.DeclarativeContainer):
    """Улучшенный контейнер зависимостей"""

    # Конфигурации
    config = providers.Singleton(BaseConfig)
    data_config = providers.Singleton(DataConfig)
    recommendation_config = providers.Singleton(RecommendationConfig)

    # Репозитории (Singleton - одна инстанция на приложение)
    movie_repository = providers.Singleton(
        CachedMovieRepository,
        data_config=data_config,
    )

    quote_repository = providers.Singleton(
        CachedQuoteRepository,
        data_config=data_config,
    )

    recommendation_repository = providers.Singleton(
        TfidfRecommendationRepository,
        movie_repository=movie_repository,
    )

    # Сервисы (Prototype - новый экземпляр для каждого запроса)
    movie_service = providers.Factory(
        MovieService,
        movie_repository=movie_repository,
    )

    recommendation_service = providers.Factory(
        RecommendationService,
        movie_repository=movie_repository,
        recommendation_repository=recommendation_repository,
        recommendation_config=recommendation_config,
    )

    genre_service = providers.Singleton(
        GenreClassificationService,
    )

    quote_service = providers.Factory(
        QuoteService,
        quote_repository=quote_repository,
    )
