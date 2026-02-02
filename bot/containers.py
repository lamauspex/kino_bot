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

    # Конфигурации (уже инициализированные объекты)
    bot_config = providers.Object(settings.bot)
    config = providers.Object(BaseConfig)
    data_config = providers.Object(settings.data)
    cache_config = providers.Object(settings.cache)
    performance_config = providers.Object(settings.performance)
    recommendations_config = providers.Object(settings.recommendations)
    ml_config = providers.Object(settings.ml)

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
        recommendations_config=recommendations_config,
    )

    # Сервисы (Prototype - новый экземпляр для каждого запроса)
    movie_service = providers.Factory(
        MovieService,
        movie_repository=movie_repository,
        performance_config=performance_config,
    )

    recommendation_service = providers.Factory(
        RecommendationService,
        movie_repository=movie_repository,
        recommendation_repository=recommendation_repository,
        recommendations_config=recommendations_config,
    )

    genre_service = providers.Factory(
        GenreClassificationService,
        ml_config=ml_config,
        performance_config=performance_config,
    )

    quote_service = providers.Factory(
        QuoteService,
        quote_repository=quote_repository,
        cache_config=cache_config,
    )

    # Обработчики (Prototype - новый экземпляр для каждого запроса)
    callback_handler = providers.Factory(
        'bot.handlers.callback.main.CallbackHandler',
        movie_service=movie_service,
        recommendation_service=recommendation_service,
        genre_service=genre_service,
    )

    text_handler = providers.Factory(
        'bot.handlers.text.main.TextHandler',
        movie_service=movie_service,
        genre_service=genre_service,
        recommendation_service=recommendation_service,
    )


container = EnhancedContainer()
