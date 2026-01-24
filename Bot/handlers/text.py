""" Текстовый ввод """


from bot.Function.movie_info import get_movie_info
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


from model_fit.Genre_Classification_Function import load_model_predict
from bot.utils.Recommendation_System_Function import get_recommendations


async def handle_user_input(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    """ Обработчик текста """

    user_message = update.message.text
    print("Получен текст от пользователя:", user_message)

    # Ввод пользователем название фильма
    if user_message.startswith('Расскажи о фильме'):
        movie_title = user_message[len('Расскажи о фильме'):].strip()
        print(f"Запрос информации о фильме: {movie_title}")

        movie_info, reply_markup = await get_movie_info(movie_title)

        await update.message.reply_text(
            movie_info,
            reply_markup=reply_markup
        )
        return

    # Поиск подходящего жанра
    elif context.user_data.get('search_genre_action'):
        # Обработка сюжета
        await update.message.reply_text('Обрабатываю сюжет...')

        # Здесь вызываем функцию для предсказания жанра
        predicted_genre = load_model_predict(user_message)
        context.user_data['predicted_genre'] = predicted_genre

        await update.message.reply_text(f"Это похоже на {predicted_genre}")

        keyboard = [
            [InlineKeyboardButton(
                "Да",
                callback_data='search_movies'
            )],
            [InlineKeyboardButton(
                "В меню",
                callback_data='main_menu'
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "Поищем фильмы в этом жанре?",
            reply_markup=reply_markup
        )

        # Сбрасываем состояние
        context.user_data['search_genre_action'] = False

    # Поис похожих фильмов
    elif context.user_data.get('similar_movie_action'):

        # Обработка похожего фильма
        title = user_message
        recommendations = get_recommendations(title)

        # Проверяем, есть ли похожие фильмы
        if not recommendations:
            await update.message.reply_text(
                text="К сожалению, похожих фильмов не найдено."
            )

        else:
            formated_recommendations = [
                f"{name} ({url})" for name, url in recommendations
            ]
            await update.message.reply_text(
                text=f"Похожие фильмы: {', '.join(formated_recommendations)}"
            )

        keyboard = [
            [InlineKeyboardButton(
                "Еще варианты",
                callback_data='search_movies'
            )],
            [InlineKeyboardButton(
                "В меню",
                callback_data='main_menu'
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "Что делаем дальше?",
            reply_markup=reply_markup
        )

        # Сбрасываем состояние
        context.user_data['similar_movie_action'] = False
