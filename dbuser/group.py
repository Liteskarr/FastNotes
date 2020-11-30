"""
Модуль, отвечающий за взаимодействие с данными групп в SQL-таблице.
"""

from typing import List, Dict

from dbuser.connection_interface import ConnectionInterface
from structures.group import GroupData

group_creation_request = """
INSERT INTO groups(name)
VALUES(?);
"""

getting_group_by_id_request = """
SELECT * FROM groups
WHERE id = ?;
"""

getting_all_groups_request = """
SELECT DISTINCT * FROM groups
"""

updating_group_name = """
UPDATE groups
SET name = ?
WHERE id = ?;
"""

deleting_group_request = """
DELETE FROM groups
WHERE
    id = ?;
"""


class GroupsUser(ConnectionInterface):
    def __init__(self):
        super().__init__()

    def create_new_group(self, name: str) -> None:
        cursor = self.cursor()
        cursor.execute(group_creation_request, (name,))

    def get_group_by_id(self, id_: int) -> GroupData:
        cursor = self.cursor()
        result = cursor.execute(getting_group_by_id_request, (id_,)).fetchone()
        return GroupData.from_tuple(result)

    def get_all_groups(self) -> List[GroupData]:
        cursor = self.cursor()
        return list(map(GroupData.from_tuple, cursor.execute(getting_all_groups_request).fetchall()))

    def get_groups_dict(self) -> Dict[int, GroupData]:
        cursor = self.cursor()
        return dict(((int(k), GroupData(int(k), v)) for k, v in cursor.execute(getting_all_groups_request)))

    def update_group_name(self, id_: int, name: str) -> None:
        cursor = self.cursor()
        cursor.execute(updating_group_name, (name, id_,))

    def delete_group_by_id(self, id_: int) -> None:
        cursor = self.cursor()
        cursor.execute(deleting_group_request, (id_,))
