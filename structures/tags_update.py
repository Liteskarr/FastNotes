from typing import List
from dataclasses import dataclass, field


@dataclass
class TagsUpdate:
    note_id: int
    added: List[str] = field(default_factory=list)
    deleted: List[str] = field(default_factory=list)
