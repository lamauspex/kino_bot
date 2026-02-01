""" Kонтейнер зависимостей """

from dependency_injector import containers, providers

from .config import settings, BaseConfig
from .repositories import (
    TfidfRecommendationRepository,
    CachedQuoteRepository,
    CachedMovieRepository
)
from .services import (
    GenreClassificationService,
    QuoteService,
    RecommendationService,
    MovieService
)


class EnhancedContainer(containers.DeclarativeContainer):

    # Конфигурации
    bot_config = providers.Singleton(settings.bot)
    config = providers.Singleton(BaseConfig)
    data_config = providers.Singleton(settings.data_config)
    recommendation_config = providers.Singleton(settings.recomm_config)

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
        service_config=settings.service_config
    )

    quote_service = providers.Factory(
        QuoteService,
        quote_repository=quote_repository,
    )


container = EnhancedContainer()
