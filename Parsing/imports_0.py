from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    # Настройка драйвера
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Используем WebDriverManager для установки драйвера
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()),
        options=options
    )
    return driver
