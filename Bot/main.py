
# Главный файл для запуска бота

from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes, ApplicationBuilder, MessageHandler, filters, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import TOKEN 

from Function.Recommendations_Genre_Function import get_recommendations_genre
from Function.Recommendation_System_Function import get_recommendations
from Function.Genre_Classification_Function import load_model_predict
from Function.Get_movie_info import get_movie_info
from Function.Random_Function import get_random_movie
from Function.Get_search_movies import search_movies
from Function.Random_Quote import get_random_quote
from Function.imports_1 import *
import nest_asyncio
import asyncio

dk = pd.read_csv('Data\\quotes.csv')
nest_asyncio.apply()


# Приветствие
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    welcome_message = (
        "Hello! Я твой Kино-бот! Я могу найти фильм, рассказать о нем," 
        "подобрать похожий и не только. Нажимай далее и Я все устрою\n"
        "Также, Ты можешь просто написать 'Расскажи о фильме ...'"
        )
    
    keyboard = [[InlineKeyboardButton("Далее", callback_data='main_menu')]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)  
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


# Меню 
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    quote = get_random_quote(dk)
    await update.message.reply_text(quote)

    keyboard = [
        [InlineKeyboardButton("Найти фильм по жанру", callback_data='search_genre')],
        [InlineKeyboardButton("Случайный фильм", callback_data='random_movie')],
        [InlineKeyboardButton("Подобрать похожий фильм", callback_data='similar_movie')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери действие:", reply_markup=reply_markup)


# Обработка нажатий на кнопки
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
            f"А вот ссылка на этот фильм: {random_movie[3]}"))
        
        keyboard = [
            [InlineKeyboardButton("Попробуем еще", callback_data='random_movie')],
            [InlineKeyboardButton("Меню", callback_data='main_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Что делаем дальше?", reply_markup=reply_markup)
    
    # Кнопка "Поиска по жанру"
    elif query.data == 'search_genre':
        context.user_data['search_genre_action'] = True
        await query.message.reply_text(text='Опиши свой сюжет, ключевые моменты')
        return # Ждём ответа от пользователя
    
    # Кнопка "Подобрать похожий фильм"
    elif query.data == 'similar_movie':
        context.user_data['similar_movie_action'] = True
        await query.message.reply_text(text='Назови фильм а я найду похожие')
        return # Ждём ответа от пользователя


# Обработчик текста 
async def handle_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    print("Получен текст от пользователя:", user_message)
    
    # Ввод пользователем название фильма
    if user_message.startswith('Расскажи о фильме'):
        movie_title = user_message[len('Расскажи о фильме'):].strip()
        print(f"Запрос информации о фильме: {movie_title}")
        
        movie_info, reply_markup = await get_movie_info(movie_title)
        
        await update.message.reply_text(movie_info, reply_markup=reply_markup)
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
            [InlineKeyboardButton("Да", callback_data='search_movies')],
            [InlineKeyboardButton("В меню", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text("Поищем фильмы в этом жанре?", reply_markup=reply_markup)
        
        context.user_data['search_genre_action'] = False  # Сбрасываем состояние

    # Поис похожих фильмов
    elif context.user_data.get('similar_movie_action'):
        # Обработка похожего фильма
        title = user_message
        recommendations = get_recommendations(title)
        
        # Проверяем, есть ли похожие фильмы
        if not recommendations:
            await update.message.reply_text(text="К сожалению, похожих фильмов не найдено.")
        
        else:
            formated_recommendations = [f"{name} ({url})" for name, url in recommendations]
            await update.message.reply_text(text=f"Похожие фильмы: {', '.join(formated_recommendations)}")
        
        keyboard = [
            [InlineKeyboardButton("Еще варианты", callback_data='search_movies')],
            [InlineKeyboardButton("В меню", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text("Что делаем дальше?", reply_markup=reply_markup)
        
        context.user_data['similar_movie_action'] = False  # Сбрасываем состояние



# Функция для получения информации о фильме
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
            [InlineKeyboardButton("В меню", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        return movie_info, reply_markup 
        
    else:
        return "Фильм не найден"
    
    
    






async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_input, block=True))

    print("Бот запущен и готов к работе!")
    await app.run_polling()
    
    

if __name__ == "__main__":
    asyncio.run(main()) 
 
