
import pandas as pd
import re


# Загружаем данные
df = pd.read_csv('Data\\top_movies.csv')

# Заменяем NaN на пустые строки
df['description'] = df['description'].fillna("")

# Удаляем строки с пустыми значениями в колонке 'description'
df.dropna(subset=['description'], inplace=True)

# Приводим столбец 'description' к типу строк
df['description'] = df['description'].astype(str)

# Список слов для удаления
stop_words = list({'на', 'не', 'он', 'его', 'что', 'из',
                  'по', 'за', 'чтобы', 'во', 'так', 'после',
                   'где', 'только', 'это', 'то', 'она', 'они',
                   'ее', 'но', 'как', 'от', 'их', 'для', 'ему',
                   'все', 'когда', 'который', 'своей', 'со',
                   'до', 'может', 'уже', 'один', 'под'})


# Функция для предобработки текста
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s', ' ', text)
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text.strip()


# Применяем предобработку к столбцу description
df['description'] = df['description'].apply(preprocess_text)
