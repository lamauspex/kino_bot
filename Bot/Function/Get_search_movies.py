
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from Function.Recommendations_Genre_Function import get_recommendations_genre
from Function.imports_1 import *
import nest_asyncio


dk = pd.read_csv('Data\\quotes.csv')
nest_asyncio.apply()


# Поиск фильмов по жанру
async def search_movies(query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE) -> None:
    await query.answer()   
    context.user_data['search_genre_action'] = None
    
    predicted_genre = context.user_data.get('predicted_genre')
    recommendations = get_recommendations_genre(predicted_genre)

    if not recommendations:
        await query.message.reply_text("К сожалению, не удалось найти фильмы в этом жанре.")
        return
    else:
        recommendations_text = "\n".join(recommendations)
        await query.message.reply_text(
            f"\n\nВот что я нашел:\n{recommendations_text}"
            f"\nТы можешь спросить меня о любом фильме."
            f"\nПросто напиши: 'Расскажи о ...'\n"
            )
        
        keyboard = [
            [InlineKeyboardButton("Еще варианты", callback_data='search_movies')],
            [InlineKeyboardButton("В меню", callback_data='main_menu')]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text("Как поступим дальше?", reply_markup=reply_markup)
        
        context.user_data['search_genre_action'] = False  # Сбрасываем состояние
