from dataclasses import dataclass
from typing import List, Tuple

from src.structures.abstract_data import AbstractData
from src.structures.note import NoteData


@dataclass
class NoteWithTags(AbstractData):
    """
    Класс-контейнер для данных заметки вместе с ее тегами.
    """

    data: NoteData
    tags: List[str]

    @staticmethod
    def from_tuple(tuple_: Tuple):
        note = super(NoteWithTags).from_tuple(tuple_[:-1])
        tags = list(tuple_[-1])
        return NoteWithTags(note, tags)
