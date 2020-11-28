import sqlite3
from typing import List, Dict

from dbuser.connection_interface import ConnectionInterface


getting_all_tags_by_note_id_request = """
SELECT tags.name FROM notes_tags
INNER JOIN tags ON notes_tags.tag = tags.id
WHERE
    notes_tags.note = ?;
"""

getting_tag_by_name_request = """
SELECT id FROM tags
WHERE
    name = ?;
"""

getting_all_tags_request = """
SELECT * FROM tags;
"""

creating_tag_request = """
INSERT INTO tags(name)
VALUES(?);
"""

connecting_tag_with_note_id_request = """
INSERT INTO notes_tags
VALUES(?, ?);
"""

disconnecting_tag_by_name_and_note_id_request = """
DELETE FROM notes_tags
WHERE
    note = ?
    AND
    tag = (SELECT id FROM tags WHERE name = ?);
"""

disconnecting_tags_by_group_id_request = """
DELETE FROM notes_tags
WHERE
    note IN (
        SELECT id FROM notes
        WHERE
            [group] = ?
    );
"""


class TagUser(ConnectionInterface):
    def __init__(self):
        self._existing_tags = dict()
        super().__init__()

    def set_connection(self, connection: sqlite3.Connection) -> None:
        super(TagUser, self).set_connection(connection)
        self._existing_tags = self.get_all_tags()

    def get_all_tags(self) -> Dict[int, str]:
        cursor = self.cursor()
        return dict((k, v) for k, v in cursor.execute(getting_all_tags_request).fetchall())

    def get_all_tags_by_note_id(self, note_id: int) -> List[str]:
        cursor = self.cursor()
        return list(map(lambda x: x[0],
                        cursor.execute(getting_all_tags_by_note_id_request, (note_id, )).fetchall()))

    def get_tag_id_by_name(self, tag: str) -> int:
        cursor = self.cursor()
        return cursor.execute(getting_tag_by_name_request, (tag, )).fetchone()[0]

    def create_tag(self, tag: str) -> None:
        cursor = self.cursor()
        cursor.execute(creating_tag_request, (tag, ))
        self._existing_tags = self.get_all_tags()

    def create_tag_if_does_not_exist(self, tag: str) -> None:
        if tag not in self._existing_tags.values():
            self.create_tag(tag)
            self.commit()

    def collect_rubbish(self) -> None:
        raise NotImplementedError()

    def connect_tags_with_note_by_id(self, note_id: int, tags: List[str]) -> None:
        cursor = self.cursor()
        for tag in tags:
            self.create_tag_if_does_not_exist(tag)
            tag_id = cursor.execute(getting_tag_by_name_request, (tag, )).fetchone()[0]
            cursor.execute(connecting_tag_with_note_id_request, (note_id, tag_id, ))

    def disconnect_tags_by_names_and_note_id(self, note_id: int, tags: List[str]) -> None:
        cursor = self.cursor()
        for tag in tags:
            cursor.execute(disconnecting_tag_by_name_and_note_id_request, (note_id, tag, ))

    def disconnect_tags_by_group_id(self, group_id) -> None:
        cursor = self.cursor()
        cursor.execute(disconnecting_tags_by_group_id_request, (group_id, ))
