"""
Модуль, содержащий абстрактный класс, которые определяет поведение класса данных.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class AbstractData:
    @staticmethod
    def from_tuple(tuple_: Tuple):
        """
        Загружает объект из кортежа.
        :param tuple_: Кортеж с данными.
        """
        raise NotImplementedError()
