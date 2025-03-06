
# Функция "Рекомендательная система"

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import random
import re



# Загружаем данные
df = pd.read_csv('Data\\top_movies.csv')
# Удаляем строки с пустыми значениями в колонке 'description'
df.dropna(subset=['description'], inplace=True)

# Список слов для удаления
stop_words = list({'на', 'не', 'он', 'его', 'что', 'из', 
                  'по', 'за', 'чтобы', 'во', 'так', 'после', 
                  'где', 'только', 'это', 'то', 'она', 'они', 
                  'ее', 'но', 'как', 'от', 'их', 'для', 'ему',
                  'все', 'когда', 'который', 'своей', 'со',
                  'до', 'может', 'уже', 'один', 'под' })

# Функция для предобработки текста
def preprocess_text(text):
  text = text.lower()
  text = re.sub(r'\W+', ' ', text)
  text = re.sub(r'\s', ' ', text)
  text = ' '.join([word for word in text.split() if word not in stop_words])
  return text.strip()

# Применяем предобработку к столбцу description
df['description'] = df['description'].apply(preprocess_text)

# Векторизация описаний
tfidf = TfidfVectorizer(stop_words='english')
tfidfmatrix = tfidf.fit_transform(df['description'])

# Вычисление косинусного сходства
cosine_sim = linear_kernel(tfidfmatrix, tfidfmatrix)

# Список для показанных фильмов
shown_movies = set()

# Функция для получения рекомендаций
def get_recommendations(title, cosinesim=cosine_sim):
    idx = df.index[df['title'] == title].tolist()[0]         # Получаем индекс фильма
    simscores = list(enumerate(cosinesim[idx]))                      # Получаем оценки схожести
    simscores = sorted(simscores, key=lambda x: x[1], reverse=True)  # Сортируем

    # Фильтруем уже показанные фильмы
    simscores = [score for score in simscores if score[0] not in shown_movies] 
    if not simscores:
      return []

    random.shuffle(simscores)    
    simscores = simscores[:4]                  # Берем топ-3
    movie_indices = [i[0] for i in simscores]   # Получаем индексы

    # Добавляем показанные фильмы в список
    shown_movies.update(movie_indices)

    # Формируем вывод с названиями и ссылками
    recommendations = [(df['title'].iloc[i],df['link'].iloc[i]) for i in movie_indices]
    return recommendations  # Возвращаем названия фильмов и ссылки 


# Пример вызова функции
# print(get_recommendations('Зеленая миля'))