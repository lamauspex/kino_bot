import pandas as pd
import random


#  Функция, которая случайным образом выбирает цитату и автора

# Получаем путь к текущему файлу
dk = pd.read_csv('Data\\quotes.csv')


def get_random_quote(quotes_df):
    # Выбираем случайную строку
    random_quote = quotes_df.sample(1).iloc[0]
    return f"...{random_quote['phrase']}...\n{random_quote['author']}"

# print(get_random_quote(dk))
