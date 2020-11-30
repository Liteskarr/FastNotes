"""
Интерфес для взаимодействия с базой данных.
"""

import sqlite3


class ConnectionInterface:
    def __init__(self):
        self.connection: sqlite3.Connection

    def set_connection(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def close(self) -> None:
        self.connection.close()

    def commit(self) -> None:
        self.connection.commit()

    def rollback(self) -> None:
        self.connection.rollback()

    def cursor(self) -> sqlite3.Cursor:
        return self.connection.cursor()
