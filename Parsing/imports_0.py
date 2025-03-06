from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os


def setup_driver():
    # Настройка драйвера
    options = Options()
    options.add_argument('--no-sandbox')  
    options.add_argument('--disable-dev-shm-usage')

    # Используем WebDriverManager для установки драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

