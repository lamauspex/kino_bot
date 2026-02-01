"""Стратегии callback'ов"""

from .navigation import MainMenuStrategy
from .search import SearchMoviesStrategy, RandomMovieStrategy
from .genre import SearchGenreStrategy
from .similar import SimilarMovieStrategy, TfidfSimilarStrategy
from .recommendations import GetRecommendationsStrategy

__all__ = [
    'MainMenuStrategy',
    'SearchMoviesStrategy',
    'RandomMovieStrategy',
    'SearchGenreStrategy',
    'SimilarMovieStrategy',
    'TfidfSimilarStrategy',
    'GetRecommendationsStrategy',
]
