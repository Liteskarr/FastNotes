"""
Модуль, отвечающий за взаимодействие с данными напоминаний SQL-таблицы.
"""

from typing import List

from src.consts import DATETIME_FORMAT
from src.dbuser.connection_interface import ConnectionInterface
from src.structures.notice import NoticeData

getting_unread_notices_request = """
SELECT * FROM notices 
WHERE
    is_read = FALSE;
"""

getting_notice_by_id_request = """
SELECT * FROM notices
WHERE
    id = ?;
"""

adding_notice_request = """
INSERT INTO notices(note, description, date, is_read)
VALUES(?, ?, ?, ?);
"""

reading_notice_by_id_request = """
UPDATE notices
SET is_read = TRUE
WHERE id = ?;
"""


class NoticeUser(ConnectionInterface):
    def get_unread_notices_ordered_by_date(self) -> List[NoticeData]:
        """
        Возвращает список непрочитанных оповещений, отсортированных по дате.
        """
        cursor = self.cursor()
        data = list(map(NoticeData.from_tuple, cursor.execute(getting_unread_notices_request).fetchall()))
        return sorted(data, key=lambda x: x.date)

    def get_notice_by_id(self, notice_id: int) -> NoticeData:
        """
        Возвращает оповещение по его ID.
        :param notice_id: ID оповещения.
        """
        cursor = self.cursor()
        return NoticeData.from_tuple(cursor.execute(getting_notice_by_id_request, (notice_id,)).fetchone())

    def add_notice(self, notice: NoticeData) -> None:
        """
        Добавляет оповещение по его данным.
        :param notice: Данные оповещения.
        """
        cursor = self.cursor()
        cursor.execute(adding_notice_request, (notice.note.id,
                                               notice.description,
                                               notice.date.strftime(DATETIME_FORMAT),
                                               notice.is_read))

    def read_notice(self, notice_id: int) -> None:
        """
        Делает оповещение прочитанным по его ID.
        :param notice_id: ID оповещения.
        """
        cursor = self.cursor()
        cursor.execute(reading_notice_by_id_request, (notice_id,))
