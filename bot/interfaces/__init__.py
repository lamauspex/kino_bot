from .interfaces_repo import (
    MovieRepositoryProtocol,
    QuoteRepositoryProtocol,
    RecommendationRepositoryProtocol
)
from .interfaces_service import (
    MovieServiceProtocol,
    QuoteServiceProtocol,
    RecommendationServiceProtocol,
    GenreClassificationServiceProtocol
)

__all__ = [
    'MovieRepositoryProtocol',
    'QuoteRepositoryProtocol',
    'RecommendationRepositoryProtocol',
    'MovieServiceProtocol',
    'QuoteServiceProtocol',
    'RecommendationServiceProtocol',
    'GenreClassificationServiceProtocol'
]
