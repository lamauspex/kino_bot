"""Конфигурация данных: загрузка CSV-файлов."""

import pandas as pd
from pydantic import Field

from .base import BaseConfig


class DataConfig(BaseConfig):
    """ Загрузка данных из CSV """

    DATA_QUOTES_PATH: str = Field(description='Путь к файлу цитат')
    DATA_MOVIES_PATH: str = Field(description='Путь к файлу фильмов')

    @property
    def DATA_QUOTES(self) -> pd.DataFrame:
        """ Цитаты """
        return pd.read_csv(self.DATA_QUOTES_PATH)

    @property
    def DATA_MOVIES(self) -> pd.DataFrame:
        """ Фильмы """
        return pd.read_csv(self.DATA_MOVIES_PATH)


data_config = DataConfig.create()
