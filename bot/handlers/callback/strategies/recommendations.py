""" Стратегии для обработки callback queries """


from telegram.ext import ContextTypes
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from bot.handlers.base.results import CallbackAction, HandlerResult
from bot.handlers.callback.strategies.navigation import BaseCallbackStrategy


class GetRecommendationsStrategy(BaseCallbackStrategy):
    """Стратегия получения рекомендаций"""

    async def execute(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> HandlerResult:
        await update.callback_query.answer()

        # Логика получения рекомендаций
        recommendations = await self._recommendation_service.get_similar_movies(
            context.user_data.get('last_movie', ''),
            limit=5
        )

        if not recommendations:
            return HandlerResult(text="Не удалось найти рекомендации")

        text = "Похожие фильмы:\n" + "\n".join(
            f"{name} ({url})" for name, url in recommendations
        )

        keyboard = [
            [InlineKeyboardButton(
                "Ещё",
                callback_data='get_recommendations'
            )],
            [InlineKeyboardButton(
                "В меню",
                callback_data='main_menu'
            )],
        ]

        return HandlerResult(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    def can_handle(self, callback_data: str) -> bool:

        return callback_data == CallbackAction.GET_RECOMMENDATIONS.value
