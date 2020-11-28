from dataclasses import dataclass
from datetime import datetime
from typing import Tuple

import consts
from structures.abstract_data import AbstractData


@dataclass
class NoteData(AbstractData):
    id: int = 0
    name: str = ''
    text: str = ''
    creation_date: datetime = None
    editing_date: datetime = None
    group: int = 0

    @staticmethod
    def from_tuple(tuple_: Tuple[int, str, str, int, int, int]):
        note = NoteData(*tuple_)
        note.creation_date = datetime.strptime(str(note.creation_date), consts.DATETIME_FORMAT)
        note.editing_date = datetime.strptime(str(note.editing_date), consts.DATETIME_FORMAT)
        return note
