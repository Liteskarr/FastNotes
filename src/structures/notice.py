from dataclasses import dataclass
from datetime import datetime
from typing import Tuple

from src.structures.abstract_data import AbstractData
from src.structures.note import NoteData
from src.consts import DATETIME_FORMAT


@dataclass
class NoticeData(AbstractData):
    """
    Класс-контейнер для данных напоминания.
    """

    id: int
    note: NoteData
    description: str
    date: datetime
    is_read: bool = False

    @staticmethod
    def from_tuple(tuple_: Tuple):
        notice = NoticeData(*tuple_)
        notice.date = datetime.strptime(str(notice.date), DATETIME_FORMAT)
        return notice
