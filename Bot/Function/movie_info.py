""" Получение информации о фильме """

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def get_movie_info(movie_title):
    movie_data = df.loc[df['title'] == movie_title]

    if not movie_data.empty:
        movie_info = (
            f"\n{movie_data['title'].values[0]}"
            f"\n{movie_data['genre'].values[0]}"
            f"\n{movie_data['director'].values[0]}"
            f"\n{movie_data['link'].values[0]}"
            f"\n{movie_data['description'].values[0]}\n"
        )

        keyboard = [
            [InlineKeyboardButton(
                "В меню",
                callback_data='main_menu'
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        return movie_info, reply_markup

    else:
        return "Фильм не найден"
