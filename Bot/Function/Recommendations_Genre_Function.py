
# Функция для рекомендаций фильмов по жанру

from Function.imports_1 import *

num_recommendations = 5

def get_recommendations_genre(input_genre):
    recomm = df[df['genre'] == input_genre]['title'].to_list()
    
    if not recomm:
        return []
    return random.sample(recomm, min(num_recommendations, len(recomm)))