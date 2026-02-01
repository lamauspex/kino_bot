"""Валидаторы для обработчиков"""

import re
from typing import Optional


def validate_movie_title(title: str) -> bool:
    """Валидация названия фильма"""

    if not title or len(title.strip()) < 2:
        return False

    # Не должен содержать только спецсимволы
    clean_title = re.sub(r'[^\w\s]', '', title)

    return len(clean_title.strip()) >= 2


def validate_genre_description(description: str) -> bool:
    """Валидация описания жанра"""

    if not description or len(description.strip()) < 10:
        return False

    # Должен содержать хотя бы несколько слов
    words = description.strip().split()
    return len(words) >= 3


def validate_callback_data(callback_data: str) -> bool:
    """Валидация callback data"""

    if not callback_data:
        return False

    # Должен содержать только безопасные символы
    safe_pattern = re.compile(r'^[a-zA-Z0-9_:\-\.]+$')
    return bool(safe_pattern.match(callback_data))


def sanitize_user_input(user_input: str) -> str:
    """Очистка пользовательского ввода"""

    if not user_input:
        return ""

    # Убираем лишние пробелы и приводим к нижнему регистру
    cleaned = ' '.join(user_input.split())

    # Убираем потенциально опасные символы
    cleaned = re.sub(r'[<>"\']', '', cleaned)

    return cleaned.strip()


def is_command(text: str) -> bool:
    """Проверить, является ли текст командой"""

    return text.startswith('/') and len(text.strip()) > 1


def extract_command_name(command_text: str) -> Optional[str]:
    """Извлечь название команды"""

    if is_command(command_text):
        # Убираем / и возможные параметры
        parts = command_text.split()
        if parts:
            return parts[0][1:]  # Убираем /
    return None
