from typing import List

from dbuser.connection_interface import ConnectionInterface
from structures.notice import NoticeData

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
        cursor = self.cursor()
        data = list(map(NoticeData.from_tuple, cursor.execute(getting_unread_notices_request).fetchall()))
        return sorted(data, key=lambda x: x.date)

    def get_notice_by_id(self, id_: int) -> NoticeData:
        cursor = self.cursor()
        return NoticeData.from_tuple(cursor.execute(getting_notice_by_id_request, (id_,)).fetchone())

    def add_notice(self, notice: NoticeData) -> None:
        cursor = self.cursor()
        cursor.execute(adding_notice_request, (notice.note.id,
                                               notice.description,
                                               notice.date.strftime('%Y%m%d%H%M'),
                                               notice.is_read))

    def read_notice(self, id_: int) -> None:
        cursor = self.cursor()
        cursor.execute(reading_notice_by_id_request, (id_,))
