""" Слой доступа к данным """

from typing import List, Optional, Protocol

from bot.models.movie import (
    Movie,
    Quote,
    MovieRecommendation
)


class MovieRepositoryProtocol(Protocol):
    """Интерфейс репозитория фильмов"""

    async def get_by_id(
        self, movie_id: str
    ) -> Optional[Movie]: ...

    async def get_by_title(
        self, title: str
    ) -> Optional[Movie]: ...

    async def search_by_genre(
        self, genre: str, limit: int = 10
    ) -> List[Movie]: ...

    async def get_random(self) -> Movie: ...

    async def search_by_title_contains(
        self, query: str, limit: int = 10
    ) -> List[Movie]: ...


class QuoteRepositoryProtocol(Protocol):
    """Интерфейс репозитория цитат"""

    async def get_random(self) -> Quote: ...


class RecommendationRepositoryProtocol(Protocol):
    """Интерфейс репозитория рекомендаций"""

    async def get_similar_movies(
        self,
        movie: Movie,
        limit: int = 5
    ) -> List[MovieRecommendation]: ...

    async def get_by_genre(
        self,
        genre: str,
        limit: int = 5
    ) -> List[Movie]: ...
