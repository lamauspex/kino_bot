"""Dependency Injection контейнер"""

from dependency_injector import containers, providers

from .config.base import BaseConfig
from .config.bot_config import BotConfig
from .config.data_config import DataConfig
from .config.recom_config import RecommendationConfig

from .services.movie_service import MovieService
from .services.quote_service import QuoteService
from .services.recommendation_service import RecommendationService
from .services.genre_classification_service import GenreClassificationService
from .services.tfidf_recommendation_service import TfidfRecommendationService

from .handlers.base.base import AbstractHandler
from .handlers.command.start import StartHandler
from .handlers.command.menu import MenuHandler
from .handlers.callback.callbacks import CallbackHandler
from .handlers.text.text import TextHandler


class Container(containers.DeclarativeContainer):
    """Центральный контейнер зависимостей"""

    # Конфигурации (singleton - создаются один раз)
    config = providers.Singleton(
        BaseConfig,
    )

    bot_config = providers.Singleton(
        BotConfig,
    )

    data_config = providers.Singleton(
        DataConfig,
    )

    recommendation_config = providers.Singleton(
        RecommendationConfig,
    )

    # Сервисы (singleton - одна инстанция на всё приложение)
    movie_service = providers.Singleton(
        MovieService,
        data_config=data_config,
    )

    quote_service = providers.Singleton(
        QuoteService,
        data_config=data_config,
    )

    recommendation_service = providers.Singleton(
        RecommendationService,
        movie_service=movie_service,
        config=recommendation_config,
    )

    genre_service = providers.Singleton(
        GenreClassificationService,
    )

    tfidf_service = providers.Singleton(
        TfidfRecommendationService,
    )

    # Обработчики (prototype - новый экземпляр для каждого запроса)
    start_handler = providers.Factory(
        StartHandler,
    )

    menu_handler = providers.Factory(
        MenuHandler,
        quote_service=quote_service,
        movie_service=movie_service,
    )

    callback_handler = providers.Factory(
        CallbackHandler,
        movie_service=movie_service,
        recommendation_service=recommendation_service,
        genre_service=genre_service,
        tfidf_service=tfidf_service,
    )

    text_handler = providers.Factory(
        TextHandler,
        movie_service=movie_service,
        genre_service=genre_service,
        recommendation_service=recommendation_service,
    )


# Глобальный контейнер для использования в приложении
container = Container()
