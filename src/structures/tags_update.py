from dataclasses import dataclass, field
from typing import List


@dataclass
class TagsUpdate:
    """
    Класс-контейнер для данных обновления списка тегов.
    """

    note_id: int
    added: List[str] = field(default_factory=list)
    deleted: List[str] = field(default_factory=list)
