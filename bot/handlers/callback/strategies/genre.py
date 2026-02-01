""" Стратегии для обработки callback queries """


from telegram.ext import ContextTypes
from telegram import Update

from ...base import CallbackAction, HandlerResult
from ...callback import BaseCallbackStrategy


class SearchGenreStrategy(BaseCallbackStrategy):
    """Стратегия поиска по жанру - установка состояния"""

    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> HandlerResult:
        await update.callback_query.answer()
        context.user_data['state'] = 'search_genre'

        return HandlerResult(
            text="Опишите сюжет фильма",
            should_stop=True  # Ожидаем текстовый ввод
        )

    def can_handle(self, callback_data: str) -> bool:

        return callback_data == CallbackAction.SEARCH_GENRE.value
