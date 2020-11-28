from datetime import datetime
from typing import List

import consts
from dbuser.connection_interface import ConnectionInterface
from structures.note import NoteData


creating_new_note_request = """
INSERT INTO notes(name, text, creation_date, editing_date, [group]) 
VALUES(?, '', ?, ?, ?);
"""

getting_note_by_id_request = """
SELECT * FROM notes 
WHERE
    id = ?;
"""

getting_notes_by_group = """
SELECT * FROM notes
WHERE
    [group] = ?;
"""

getting_all_notes_request = """
SELECT * FROM notes
"""

updating_note_by_data_request = """
UPDATE notes
SET
    name = ?,
    text = ?,
    creation_date = ?,
    editing_date = ?,
    [group] = ?
WHERE
    id = ?;
"""

deleting_note_by_id_request = """
DELETE FROM notes
WHERE
    id = ?;
"""

deleting_notes_by_group_id_request = """
DELETE FROM notes
WHERE
    [group] = ?;
"""


class NotesUser(ConnectionInterface):
    def create_new_note(self, name: str, group: int) -> None:
        cursor = self.cursor()
        cursor.execute(creating_new_note_request, (name,
                                                   datetime.now().strftime(consts.DATETIME_FORMAT),
                                                   datetime.now().strftime(consts.DATETIME_FORMAT),
                                                   group))

    def get_note_by_id(self, id_: int) -> NoteData:
        cursor = self.cursor()
        return NoteData.from_tuple(cursor.execute(getting_note_by_id_request, (id_, )).fetchone())

    def get_notes_by_group(self, group_id: int) -> List[NoteData]:
        cursor = self.cursor()
        return list(map(NoteData.from_tuple,
                        cursor.execute(getting_notes_by_group, (group_id, )).fetchall()))

    def get_all_notes(self) -> List[NoteData]:
        cursor = self.cursor()
        return list(map(NoteData.from_tuple, cursor.execute(getting_all_notes_request).fetchall()))

    def update_note_data(self, data: NoteData) -> None:
        cursor = self.cursor()
        cursor.execute(updating_note_by_data_request, (data.name,
                                                       data.text,
                                                       data.creation_date.strftime(consts.DATETIME_FORMAT),
                                                       data.editing_date.strftime(consts.DATETIME_FORMAT),
                                                       data.group,
                                                       data.id))

    def delete_note_by_id(self, id_: int) -> None:
        cursor = self.cursor()
        cursor.execute(deleting_note_by_id_request, (id_, ))

    def delete_notes_by_group_id(self, group_id: int) -> None:
        cursor = self.cursor()
        cursor.execute(deleting_notes_by_group_id_request, (group_id, ))
