""" Функция, которая случайным образом выбирает цитату и автора """

from bot.config.data_config import data_config


def get_random_quote():
    """ Получить случайную цитату из конфигурации """

    quotes_df = data_config.DATA_QUOTES
    random_quote = quotes_df.sample(1).iloc[0]
    return f"...{random_quote['phrase']}...\n{random_quote['author']}"
