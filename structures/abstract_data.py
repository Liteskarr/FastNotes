from dataclasses import dataclass
from typing import Tuple


@dataclass
class AbstractData:
    @staticmethod
    def from_tuple(tuple_: Tuple):
        raise NotImplementedError()
