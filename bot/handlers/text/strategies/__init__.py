"""Стратегии текстового ввода"""

from .movie_info import MovieInfoTextStrategy
from .genre_prediction import GenrePredictionTextStrategy
from .similar_movies import SimilarMovieTextStrategy

__all__ = [
    'MovieInfoTextStrategy',
    'GenrePredictionTextStrategy',
    'SimilarMovieTextStrategy',
]
