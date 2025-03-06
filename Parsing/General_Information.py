from imports_0 import *
from imports_0 import setup_driver

# Открываем страницу
url = 'https://www.kinopoisk.ru/lists/movies/top500/?utm_referrer=www.kinopoisk.ru&b=films&page=1'

# Настраиваем драйвер
driver = setup_driver()

# Список для хранения информации о фильмах
movie_data = []
page = 1

while True:
    # Формируем URL для текущей страницы
    current_url = f'https://www.kinopoisk.ru/lists/movies/top500/?utm_referrer=www.kinopoisk.ru&b=films&page={page}'
    driver.get(current_url)
    
    # Ждем, чтобы JavaScript завершил выполнение
    time.sleep(5)
    
    # Получаем HTML-код страницы
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # Находим все блоки с фильмами
    movies = soup. find_all('div', class_='styles_root__ti07r')

    # Если фильмы не найдены, значит, достигли конца
    if not movies:
        break
    
    print(f"Найдено фильмов на странице {page}: {len(movies)}")
    
    # Цикл по всем фильмам
    for movie in movies:
        # Название фильма
        title = movie.find('span', class_='styles_mainTitle__IFQyZ styles_activeMovieTittle__kJdJj').text
        
        # Страна, Жанр, Режиссёр фильма
        ganr = movie.find('a', class_='base-movie-main-info_link__YwtP1').find('span', class_='desktop-list-main-info_truncatedText__IMQRP')
        
        # Разделяем данные
        info_text = ganr.get_text().strip()
        count = info_text.split('•')
        
        country = count[0].strip()  # Страна
        genre = count[1].strip()  # Жанр
        
        # Разделяем по 'Режиссёр:' для получения информации о режиссере
        director_info = genre.split('Режиссёр:')
        genre = director_info[0].strip()  # Оставляем только жанр
        
        if len(director_info) > 1:
            director = director_info[1].strip()  # Режиссёр
        else:
            director = "Неизвестен"  # Если нет информации о режиссере
            
        # Роли
        try:
            roles_elem = movie.find('a', class_='base-movie-main-info_link__YwtP1').find_all('span', class_='desktop-list-main-info_truncatedText__IMQRP')
            if len(roles) > 1:
                roles = roles_elem[1].text 
            else:
                roles = roles_elem.text    
        except:       
            roles = "Не указано"
        # Находим год и время фильма
        data = movie.find('a', class_='base-movie-main-info_link__YwtP1').find_all('span', class_='desktop-list-main-info_secondaryText__M_aus')
            
        # Разделяем дату и время из переменной data
        mv_info = data[0].get_text().strip()
        parts = mv_info.split(', ')
        parts = [part for part in parts if part]
            
        year = parts[0].strip()      # Год
        duration = parts[1].strip()  # Время
            
        # Ссылка на фильм
        link = 'https://www.kinopoisk.ru' + movie.find('div', class_='styles_main__Y8zDm styles_mainWithBeforeSlot__JnO7X').find('a', class_='base-movie-main-info_link__YwtP1').get('href')
            
        # Сохраняем все в словарь
        movie_info = {
            'title': title,
            'country': country,
            'genre': genre,
            'director': director,
            'year': year,
            'duration': duration,
            'link': link
        }

        # Добавляем информацию о фильме в список
        movie_data.append(movie_info)
     
    # Переходим к следующей странице
    page += 1


# Закрываем драйвер
driver.quit()


# Создаем DataFrame из собранных данных
df = pd.DataFrame(movie_data)

# Указываем имя папки для DataFrame
folder_name = 'Data'
# Создаем папку, если она не существует
os.makedirs(folder_name, exist_ok=True)

# Сохраняем DataFrame в CSV файл в указанной папке
file_path = os.path.join(folder_name, 'top_movies.csv')
df.to_csv(file_path, index=False, encoding='utf-8-sig')

print(f"Данные успешно сохранены в файл {file_path}")


