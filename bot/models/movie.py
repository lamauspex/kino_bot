""" Сущности домена """


from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass(frozen=True)
class Movie:
    """Доменная модель фильма"""

    id: str
    title: str
    description: str
    genre: str
    director: str
    year: Optional[int] = None
    rating: Optional[float] = None
    link: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class MovieRecommendation:
    """Рекомендация фильма"""

    movie: Movie
    similarity_score: float
    reason: str


@dataclass(frozen=True)
class Quote:
    """Доменная модель цитаты"""

    id: str
    phrase: str
    author: str
    created_at: datetime = field(default_factory=datetime.now)
