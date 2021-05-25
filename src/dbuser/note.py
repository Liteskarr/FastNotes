"""
Модуль, отвечающий за взаимодействие с данными заметок SQL-таблицы.
"""

from datetime import datetime
from typing import List

from src import consts
from src.dbuser.connection_interface import ConnectionInterface
from src.structures.note import NoteData

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
    def create_new_note(self, name: str, group_id: int) -> None:
        """
        Создает новую заметку по имени и группе.
        :param name: Имя заметки.
        :param group_id: ID группы.
        """
        cursor = self.cursor()
        cursor.execute(creating_new_note_request, (name,
                                                   datetime.now().strftime(consts.DATETIME_FORMAT),
                                                   datetime.now().strftime(consts.DATETIME_FORMAT),
                                                   group_id))

    def get_note_by_id(self, note_id: int) -> NoteData:
        """
        Возвращает данные заметки по ее ID.
        :param note_id: ID заметки.
        """
        cursor = self.cursor()
        return NoteData.from_tuple(cursor.execute(getting_note_by_id_request, (note_id,)).fetchone())

    def get_notes_by_group(self, group_id: int) -> List[NoteData]:
        """
        Возвращает список всех заметок группы.
        :param group_id: ID группы.
        """
        cursor = self.cursor()
        return list(map(NoteData.from_tuple,
                        cursor.execute(getting_notes_by_group, (group_id,)).fetchall()))

    def get_all_notes(self) -> List[NoteData]:
        """
        Возвращает список всех заметок.
        """
        cursor = self.cursor()
        return list(map(NoteData.from_tuple, cursor.execute(getting_all_notes_request).fetchall()))

    def update_note_data(self, data: NoteData):
        """
        Обновляет данные заметки.
        :param data: Данные заметки.
        """
        cursor = self.cursor()
        cursor.execute(updating_note_by_data_request, (data.name,
                                                       data.text,
                                                       data.creation_date.strftime(consts.DATETIME_FORMAT),
                                                       data.editing_date.strftime(consts.DATETIME_FORMAT),
                                                       data.group,
                                                       data.id))

    def delete_note_by_id(self, note_id: int):
        """
        Удаляет заметку по ее ID.
        :param note_id: ID заметки.
        """
        cursor = self.cursor()
        cursor.execute(deleting_note_by_id_request, (note_id,))

    def delete_notes_by_group_id(self, group_id: int) -> None:
        """
        Удаляет заметки по группе.
        :param group_id: ID группы.
        """
        cursor = self.cursor()
        cursor.execute(deleting_notes_by_group_id_request, (group_id,))
