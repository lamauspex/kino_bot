"""Модуль обработчиков бота"""

# Импорты из базовых модулей
from .base import (
    AbstractStrategy,
    AbstractCommand,
    AbstractTextStrategy,
    HandlerResult,
    CallbackAction,
    UserState,
    KeyboardConstants,
)

# Импорты из команд
from .command import (
    start,
    main_menu,
    help_command,
    unknown_command
)

# Импорты из callback обработчиков
from .callback import (
    CallbackHandler,
    CallbackRouter
)
from .callback.strategies import (
    MainMenuStrategy,
    SearchMoviesStrategy,
    RandomMovieStrategy,
    SearchGenreStrategy,
    SimilarMovieStrategy,
    TfidfSimilarStrategy,
    GetRecommendationsStrategy,
)

# Импорты из text обработчиков
from .text import (
    TextHandler,
    TextRouter
)
from .text.strategies import (
    MovieInfoTextStrategy,
    GenrePredictionTextStrategy,
    SimilarMovieTextStrategy,
)

# Импорты из общих утилит
from .common import (
    get_main_menu_keyboard,
    get_back_keyboard,
    get_yes_no_keyboard,
    extract_movie_title,
    format_movie_recommendations,
    is_valid_movie_query,
    get_user_context_info,
    clear_user_context,
    validate_movie_title,
    validate_genre_description,
    validate_callback_data,
    sanitize_user_input,
    is_command,
    extract_command_name,
)

__all__ = [
    # Base
    'AbstractStrategy',
    'AbstractCommand',
    'AbstractTextStrategy',
    'HandlerResult',
    'CallbackAction',
    'UserState',
    'KeyboardConstants',
    # Commands
    'start',
    'main_menu',
    'help_command',
    'unknown_command',
    # Callbacks
    'CallbackHandler',
    'CallbackRouter',
    'MainMenuStrategy',
    'SearchMoviesStrategy',
    'RandomMovieStrategy',
    'SearchGenreStrategy',
    'SimilarMovieStrategy',
    'TfidfSimilarStrategy',
    'GetRecommendationsStrategy',
    # Text
    'TextHandler',
    'TextRouter',
    'MovieInfoTextStrategy',
    'GenrePredictionTextStrategy',
    'SimilarMovieTextStrategy',
    # Common
    'get_main_menu_keyboard',
    'get_back_keyboard',
    'get_yes_no_keyboard',
    'extract_movie_title',
    'format_movie_recommendations',
    'is_valid_movie_query',
    'get_user_context_info',
    'clear_user_context',
    'validate_movie_title',
    'validate_genre_description',
    'validate_callback_data',
    'sanitize_user_input',
    'is_command',
    'extract_command_name',
    # Wrapper functions - не экспортируем, создаются в app.py
]
