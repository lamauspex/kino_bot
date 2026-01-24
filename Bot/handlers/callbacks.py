
""" Кнопки (callback_query) """


from bot.Function.Random_Function import get_random_movie
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


from bot.utils.Recommendation_System_Function import get_recommendations
from bot.utils.Get_search_movies import search_movies
from bot.handlers.menu import main_menu


async def button_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    """ Обработка нажатий на кнопки """

    query = update.callback_query
    await query.answer()

    # Кнопка "Далее"
    if query.data == 'main_menu':
        await main_menu(query, context)

    # Кнопка "Да"
    elif query.data == 'search_movies':
        await search_movies(query, context)

    #  Кнопка "Еще варианты"
    elif query.data == 'get_recommendations':
        await get_recommendations(query, context)

    # Кнопка "Случайный фильм"
    elif query.data == 'random_movie':
        random_movie = get_random_movie(df)

        await query.edit_message_text(text=(
            f"Случайный фильм: {random_movie[0]}, \n"
            f"Жанр: {random_movie[2]},\n"
            f"Описание: {random_movie[1]},\n"
            f"А вот ссылка на этот фильм: {random_movie[3]}"
        ))

        keyboard = [
            [InlineKeyboardButton(
                "Попробуем еще",
                callback_data='random_movie'
            )],
            [InlineKeyboardButton(
                "Меню",
                callback_data='main_menu'
            )],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "Что делаем дальше?",
            reply_markup=reply_markup
        )

    # Кнопка "Поиска по жанру"
    elif query.data == 'search_genre':
        context.user_data['search_genre_action'] = True

        await query.message.reply_text(
            text='Опиши свой сюжет, ключевые моменты'
        )
        return  # Ждём ответа от пользователя

    # Кнопка "Подобрать похожий фильм"
    elif query.data == 'similar_movie':
        context.user_data['similar_movie_action'] = True

        await query.message.reply_text(
            text='Назови фильм а я найду похожие'
        )
        return  # Ждём ответа от пользователя
