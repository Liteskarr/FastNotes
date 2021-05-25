"""
Модуль, отвечающий за взаимодействие с данными групп в SQL-таблице.
"""

from typing import List, Dict

from src.dbuser.connection_interface import ConnectionInterface
from src.structures.group import GroupData

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
        """
        Создает новую группу по имени.
        :param name: Имя группы.
        """
        cursor = self.cursor()
        cursor.execute(group_creation_request, (name,))

    def get_group_by_id(self, group_id: int) -> GroupData:
        """
        Возвращает данные группы по ее ID.
        :param group_id: ID группы.
        """
        cursor = self.cursor()
        result = cursor.execute(getting_group_by_id_request, (group_id,)).fetchone()
        return GroupData.from_tuple(result)

    def get_all_groups(self) -> List[GroupData]:
        """
        Возвращает список всех групп.
        """
        cursor = self.cursor()
        return list(map(GroupData.from_tuple, cursor.execute(getting_all_groups_request).fetchall()))

    def get_groups_dict(self) -> Dict[int, GroupData]:
        """
        Возвращает словарь всех групп, где ключ - ID группы, а значение - ее данные.
        """
        cursor = self.cursor()
        return dict(((int(k), GroupData(int(k), v)) for k, v in cursor.execute(getting_all_groups_request)))

    def update_group_name(self, group_id: int, name: str) -> None:
        """
        Обновляет название группы по ее ID.
        :param group_id: ID группы.
        :param name: Новое имя группы.
        """
        cursor = self.cursor()
        cursor.execute(updating_group_name, (name, group_id,))

    def delete_group_by_id(self, group_id: int) -> None:
        """
        Удаляет группу по ее ID.
        :param group_id: ID группы.
        """
        cursor = self.cursor()
        cursor.execute(deleting_group_request, (group_id,))
