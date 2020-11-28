from dataclasses import dataclass
from datetime import datetime
from typing import Tuple

from structures.abstract_data import AbstractData
from structures.note import NoteData


@dataclass
class NoticeData(AbstractData):
    id: int
    note: NoteData
    description: str
    date: datetime
    is_read: bool = False

    @staticmethod
    def from_tuple(tuple_: Tuple):
        notice = NoticeData(*tuple_)
        notice.date = datetime.strptime(str(notice.date), '%Y%m%d%H%M')
        return notice
