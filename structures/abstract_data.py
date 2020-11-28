from typing import Tuple
from dataclasses import dataclass


@dataclass
class AbstractData:
    @staticmethod
    def from_tuple(tuple_: Tuple):
        raise NotImplementedError()
