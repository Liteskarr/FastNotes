from dataclasses import dataclass
from typing import List, Tuple

from structures.abstract_data import AbstractData
from structures.note import NoteData


@dataclass
class NoteWithTags(AbstractData):
    data: NoteData
    tags: List[str]

    @staticmethod
    def from_tuple(tuple_: Tuple):
        note = super(NoteWithTags).from_tuple(tuple_[:-1])
        tags = list(tuple_[-1])
        return NoteWithTags(note, tags)
