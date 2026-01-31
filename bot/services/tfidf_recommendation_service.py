""" TF-IDF рекомендательная система """

import logging
import random
import re
from typing import List, Tuple, Optional

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

logger = logging.getLogger(__name__)


class TfidfRecommendationService:
    """
    Рекомендательная система на основе TF-IDF и косинусного сходства.

    Логика:
    1. Векторизация описаний фильмов
    2. Вычисление косинусного сходства между всеми фильмами
    3. Поиск похожих фильмов по названию
    """

    def __init__(self, data_path: str = 'Data\\top_movies.csv'):
        self._data_path = data_path
        self._df: Optional[pd.DataFrame] = None
        self._cosine_sim: Optional[list] = None
        self._stop_words = {
            'на', 'не', 'он', 'его', 'что', 'из', 'по', 'за', 'чтобы',
            'во', 'так', 'после', 'где', 'только', 'это', 'то', 'она',
            'они', 'ее', 'но', 'как', 'от', 'их', 'для', 'ему', 'все',
            'когда', 'который', 'своей', 'со', 'до', 'может', 'уже',
            'один', 'под'
        }
        self._shown_movies = set()
        self._is_loaded = False

    def load(self) -> None:
        """Ленивая загрузка модели и данных"""

        if self._is_loaded:
            return

        logger.info("Загрузка TF-IDF модели...")

        self._df = pd.read_csv(self._data_path)
        self._df.dropna(subset=['description'], inplace=True)

        # Предобработка текста
        self._df['description'] = self._df['description'].apply(
            self._preprocess_text
        )

        # TF-IDF векторизация
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self._df['description'])

        # Косинусное сходство
        self._cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

        self._is_loaded = True
        logger.info("TF-IDF модель загружена")

    def _preprocess_text(self, text: str) -> str:
        """Предобработка текста"""

        text = text.lower()
        text = re.sub(r'\W+', ' ', text)
        text = re.sub(r'\s', ' ', text)
        text = ' '.join([
            word for word in text.split()
            if word not in self._stop_words
        ])
        return text.strip()

    def get_recommendations(
        self,
        title: str,
        limit: int = 4,
        exclude_shown: bool = True
    ) -> List[Tuple[str, str]]:
        """ Получить рекомендации похожих фильмов """
        self.load()

        try:
            # Находим индекс фильма
            idx_list = self._df.index[
                self._df['title'].str.lower() == title.lower()
            ].tolist()

            if not idx_list:
                logger.warning(f"Фильм не найден: {title}")
                return []

            idx = idx_list[0]

            # Получаем оценки схожести
            sim_scores = list(enumerate(self._cosine_sim[idx]))
            sim_scores = sorted(
                sim_scores,
                key=lambda x: x[1],
                reverse=True
            )

            # Исключаем уже показанные
            if exclude_shown:
                sim_scores = [
                    score for score in sim_scores
                    if score[0] not in self._shown_movies
                ]

            if not sim_scores:
                self._shown_movies.clear()  # Сброс если все показаны
                sim_scores = list(enumerate(self._cosine_sim[idx]))
                sim_scores = sorted(
                    sim_scores,
                    key=lambda x: x[1],
                    reverse=True
                )

            # Перемешиваем для разнообразия
            random.shuffle(sim_scores)

            # Берем top-N
            sim_scores = sim_scores[:limit]
            movie_indices = [i[0] for i in sim_scores]

            # Добавляем в показанные
            self._shown_movies.update(movie_indices)

            # Формируем результат
            recommendations = [
                (
                    self._df['title'].iloc[i],
                    self._df['link'].iloc[i]
                )
                for i in movie_indices
            ]

            logger.info(
                f"Найдено {len(recommendations)} рекомендаций для {title}")
            return recommendations

        except Exception as e:
            logger.error(f"Ошибка получения рекомендаций: {e}")
            return []

    def clear_shown_movies(self) -> None:
        """Очистить историю показанных фильмов"""

        self._shown_movies.clear()

    def find_by_title_contains(self, query: str) -> List[str]:
        """Поиск фильмов, содержащих запрос в названии"""

        self.load()

        matches = self._df[
            self._df['title'].str.lower().str.contains(query.lower())
        ]['title'].tolist()

        return matches[:10]
