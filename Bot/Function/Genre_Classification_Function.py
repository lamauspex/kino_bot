

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib
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
                  'все', 'когда', 'который', 'своей', 'со','с',
                  'до', 'может', 'уже', 'один', 'под', 'в', 'и', 
                  'у', 'к', 'о', 'а', 'бильбо', 'джон', 'гарри',
                  'хогвартс', 'вместе', 'него', 'которой', 'лет'
                  'год', 'вместе', 'им', 'себя', 'день', 'же'
                  'которые', 'своего', 'теперь', 'кольцо', 'будет'
                  'при', 'над', 'тот', 'пока','лишь', 'однако', 'еще'
                  'бы', 'её', 'при'})

# Функция для предобработки текста
def preprocess_text(text):
  text = text.lower()
  text = re.sub(r'\W+', ' ', text)
  text = re.sub(r'\s', ' ', text)
  text = ' '.join([word for word in text.split() if word not in stop_words])
  return text.strip()


# Применяем предобработку к столбцу description
df['description'] = df['description'].apply(preprocess_text)
# Функция "Классификация жанра фильма"


# Выбираем популярные жанры
main_genres = ['фантастика', 'драма', 'боевик', 'триллер', 'комедия', 'фэнтези']
genre_counts = df['genre'].value_counts()

filtered_data = df[df['genre'].isin(main_genres)]


# Векторизация текста
vectorizer = TfidfVectorizer()
x = vectorizer.fit_transform(filtered_data['description'])
y = filtered_data['genre']

# Разделяем данные на обучающую и тестовую выборки
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.05, random_state=42)

# Обучаем модель
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train, y_train)

#Предсказания на тестовой выборке
y_pred = model.predict(x_test)


# Оцениваем модель
# print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
# print(classification_report(y_test, y_pred))

# Сохраняем модель
joblib.dump(model, 'genre_model.joblib')
joblib.dump(vectorizer, 'vectorizer.joblib')






def load_model_predict(user_input):
    
    # Загружаем модель
    model = joblib.load('genre_model.joblib')
    vectorizer = joblib.load('vectorizer.joblib')
    
    # Векторизуем описание
    description_vectorized = vectorizer.transform([user_input])
    
    # Предсказание
    predicted_genre = model.predict(description_vectorized)
    
    return predicted_genre[0]
                           