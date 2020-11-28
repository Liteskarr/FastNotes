from dataclasses import dataclass
from typing import Tuple

from structures.abstract_data import AbstractData


@dataclass
class GroupData(AbstractData):
    id: int
    name: str

    @staticmethod
    def from_tuple(tuple_: Tuple[int, str]):
        return GroupData(*tuple_)
