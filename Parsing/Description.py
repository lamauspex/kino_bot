from imports_0 import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Устанавливаем опции для Chrome
chrome_options = Options()
chrome_options.add_argument("--headless") 

# Запускаем хром-драйвер
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


# Загружаем данные из CSV файла
df = pd.read_csv('topmovies.csv', header=None)
df.columns = ['title', 'country', 'genre', 'director', 'year', 'duration', 'link']


# Функция для парсинга описания фильма
def get_movi(url):
    if pd.isnull(url) or not url.startswith('https://'):
        print(f'НЕдействительный URL: {url}')
        return None
    try:
        print(f"Парсинг URL: {url}") 
        driver.get(url)
        
        # Явное ожидание, пока элемент не появится
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.styles_filmSynopsis__Cu2Oz')))

        # Находим описание фильма 
        description_elem = driver.find_element(By.CSS_SELECTOR, 'div.styles_filmSynopsis__Cu2Oz')
        description = description_elem.text.strip()
        return description
    
    except Exception as e:
        print(f"Ошибка при парсинге {url}: {e}")
        return None
    
        
# Добавляем новую колонку для описания
df['description'] = df['link'].apply(get_movi)

#  Сохраняем обновленный DataFrame 
df.to_csv('top_movies.csv', index=False)

# Закрываем драйвер
driver.quit()

