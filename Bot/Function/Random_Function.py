from Function.imports_1 import *

# Функция "Random"


# Функция для получения случайного фильма
def get_random_movie(df):
  random_row = df.sample()
  title = random_row['title'].values[0]
  description = random_row['description'].values[0]
  genre = random_row['genre'].values[0]
  link = random_row['link'].values[0]
  
  return title, description, genre, link



# Пример использования
# title, description, genre = get_random_movie(df)
# print(f"Вот случайный фильм:\n\nНазвание: {title}\nОписание: {description}\nЖанр: {genre}")

 
