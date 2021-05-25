"""
Интерфейс для взаимодействия с базой данных.
Позволяет скрыть функции sqlite3 и предоставить удобный
интерфейс взаимодействия.
"""

import sqlite3


class ConnectionInterface:
    def __init__(self):
        self.connection: sqlite3.Connection

    def set_connection(self, connection: sqlite3.Connection) -> None:
        """
        Устанавливает соединение с базой данных.
        :param connection: Соединение с базой данных.
        """
        self.connection = connection

    def close(self) -> None:
        """
        Закрывает соединение с базой данных.
        """
        self.connection.close()

    def commit(self) -> None:
        """
        Подтверждает изменения в базе данных.
        """
        self.connection.commit()

    def rollback(self) -> None:
        """
        Откатывает изменения в базе данных.
        """
        self.connection.rollback()

    def cursor(self) -> sqlite3.Cursor:
        """
        Возвращает объект курсора для работы с базой данных.
        """
        return self.connection.cursor()
