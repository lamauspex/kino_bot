"""Утилиты для создания клавиатур"""

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup)


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура главного меню"""
    keyboard = [
        [InlineKeyboardButton("🔍 Поиск по жанру",
                              callback_data="search_genre")],
        [InlineKeyboardButton("🎲 Случайный фильм",
                              callback_data="random_movie")],
        [InlineKeyboardButton("🔗 Похожие фильмы",
                              callback_data="similar_movie")],
        [InlineKeyboardButton(
            "✨ Рекомендации", callback_data="get_recommendations")],
    ]

    return InlineKeyboardMarkup(keyboard)


def get_back_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с кнопкой 'Назад'"""
    keyboard = [
        [InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")],
    ]

    return InlineKeyboardMarkup(keyboard)


def get_yes_no_keyboard(yes_callback: str, no_callback: str = "main_menu") -> InlineKeyboardMarkup:
    """Клавиатура с кнопками Да/Нет"""
    keyboard = [
        [InlineKeyboardButton("✅ Да", callback_data=yes_callback),
         InlineKeyboardButton("❌ Нет", callback_data=no_callback)]
    ]

    return InlineKeyboardMarkup(keyboard)
