
from typing import List, Optional, Tuple

from ..config.performance_config import PerformanceConfig
from ..models import Movie
from ..interfaces import (
    MovieServiceProtocol,
    MovieRepositoryProtocol
)


class MovieService(MovieServiceProtocol):
    """Сервис фильмов с dependency injection"""

    def __init__(
        self,
        movie_repository: MovieRepositoryProtocol,
        performance_config: PerformanceConfig
    ):
        self._movie_repository = movie_repository
        self._config = performance_config

    async def get_movie_info(
        self,
        title: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """Получить информацию о фильме"""

        try:
            movie = await self._movie_repository.get_by_title(title)

            if movie is None:
                return "Фильм не найден", None

            info_text = (
                f"🎬 *{movie.title}*\n"
                f"📚 Жанр: {movie.genre}\n"
                f"🎭 Режиссёр: {movie.director}\n"
                f"📝 {movie.description}\n"
                f"🔗 {movie.link}\n"
            )

            return info_text, "main_menu"

        except Exception as e:
            return f"Произошла ошибка при поиске фильма {e}", None

    async def get_random_movie(self) -> Movie:
        """Получить случайный фильм"""

        return await self._movie_repository.get_random()

    async def search_by_genre(self, genre: str, limit: int = 5) -> List[Movie]:
        """Поиск фильмов по жанру"""

        limit = limit or self._config.DEFAULT_SEARCH_LIMIT
        return await self._movie_repository.search_by_genre(genre, limit)
