"""Вспомогательные функции"""


from typing import Optional, List

from telegram.ext import ContextTypes


def extract_movie_title(user_message: str) -> Optional[str]:
    """Извлечь название фильма из сообщения пользователя"""

    if user_message.startswith('Расскажи о фильме'):
        return user_message[len('Расскажи о фильме'):].strip()

    # Другие паттерны извлечения названий фильмов
    patterns = [
        'расскажи о ',
        'информация о ',
        'что за фильм ',
    ]

    message_lower = user_message.lower()
    for pattern in patterns:
        if pattern in message_lower:
            return user_message[message_lower.find(pattern) + len(pattern):].strip()

    return user_message.strip()


def format_movie_recommendations(movies: List[str]) -> str:
    """Форматировать список рекомендаций фильмов"""

    if not movies:
        return "Фильмы не найдены"

    formatted = []
    for i, movie in enumerate(movies[:10], 1):  # Ограничиваем 10 фильмами
        formatted.append(f"{i}. {movie}")

    return "\n".join(formatted)


def is_valid_movie_query(message: str) -> bool:
    """Проверить, является ли сообщение валидным запросом о фильме"""

    if len(message.strip()) < 3:
        return False

    # Простая валидация - не должен содержать только цифры и спецсимволы
    clean_message = ''.join(c for c in message if c.isalnum() or c.isspace())

    return len(clean_message.strip()) >= 3


def get_user_context_info(context: ContextTypes.DEFAULT_TYPE) -> dict:
    """Получить информацию о контексте пользователя"""

    return {
        'state': context.user_data.get('state'),
        'predicted_genre': context.user_data.get('predicted_genre'),
        'last_movie': context.user_data.get('last_movie'),
        'chat_id': context.user_data.get('chat_id'),
    }


def clear_user_context(context: ContextTypes.DEFAULT_TYPE, keep_keys: Optional[List[str]] = None):
    """Очистить контекст пользователя, сохранив указанные ключи"""

    if keep_keys is None:
        keep_keys = []

    to_keep = {key: context.user_data[key]
               for key in keep_keys if key in context.user_data}
    context.user_data.clear()
    context.user_data.update(to_keep)
