""" Интерфейсы Сервисов """


from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from ..models import Movie, MovieRecommendation


class MovieServiceProtocol(ABC):
    """Интерфейс сервиса фильмов"""

    @abstractmethod
    async def get_movie_info(
        self,
        title: str
    ) -> tuple[Optional[str], Optional[str]]: ...

    @abstractmethod
    async def get_random_movie(self) -> Movie: ...

    @abstractmethod
    async def search_by_genre(
        self,
        genre: str,
        limit: int = 5
    ) -> List[Movie]: ...


class RecommendationServiceProtocol(ABC):
    """Интерфейс сервиса рекомендаций"""

    @abstractmethod
    async def get_similar_movies(
        self,
        movie_title: str,
        limit: int = 5
    ) -> List[MovieRecommendation]: ...

    @abstractmethod
    async def get_by_genre(
        self,
        genre: str,
        limit: int = None
    ) -> List[Movie]: ...


class GenreClassificationServiceProtocol(ABC):
    """Интерфейс сервиса классификации жанров"""

    @abstractmethod
    async def predict_genre(
        self,
        description: str
    ) -> Optional[str]: ...


class QuoteServiceProtocol(ABC):
    """Интерфейс сервиса цитат"""

    @abstractmethod
    async def get_random_quote(self) -> Tuple[str, str]: ...
