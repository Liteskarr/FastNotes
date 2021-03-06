"""
Модуль, представляющий из себя диалоговое окно для поиска данных по приложению.
"""

import re
import sqlite3
from typing import Tuple, List, Callable, Iterable

import PyQt5.uic as uic
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtWidgets import (QDialog,
                             QWidget,
                             QListWidgetItem)

from src import consts
from src.dbuser.group import GroupsUser
from src.dbuser.note import NotesUser
from src.dbuser.tag import TagUser
from src.structures.group import GroupData
from src.structures.note import NoteData
from src.structures.note_with_tags import NoteWithTags
from src.widgets.list_separator import ListSeparatorWidget
from src.widgets.searching_result import SearchingResultWidget

POSITION_SLICE = 20


def is_sub_sequence(original: Iterable, request: Iterable) -> bool:
    """
    Определяет, является ли одна строка подпоследовательностью другой.
    :param original: Исходная строка.
    :param request: Предполагаемая подпоследовательность.
    """
    request = iter(request)
    try:
        target = next(request)
        for element in original:
            if target == element:
                target = next(request)
        return False
    except StopIteration:
        return True


def construct_function_with_args(function, *args) -> Callable:
    def dec():
        return function(*args)

    return dec


class SearchingDialog(QDialog):
    group_chosen = pyqtSignal(int)
    note_chosen = pyqtSignal(int, int)

    def __init__(self, parent, connection: sqlite3.Connection):
        super(SearchingDialog, self).__init__(parent)
        self._connection = connection
        self._sql_notes_user = NotesUser()
        self._sql_groups_user = GroupsUser()
        self._sql_tags_user = TagUser()
        self._sql_notes_user.set_connection(self._connection)
        self._sql_groups_user.set_connection(self._connection)
        self._sql_tags_user.set_connection(self._connection)
        self._configure_ui()
        self._redraw()

    def _configure_ui(self):
        uic.loadUi('uics/search_dialog.ui', self)
        self.searching_edit.textChanged.connect(self._handle_text_changing)
        self.use_regex.clicked.connect(self._redraw)

    def _get_regex_using(self) -> bool:
        """
        Возвращает True, если поиск выполняется при помощи регулярных выражений, иначе False.
        """
        return self.use_regex.checkState()

    def _get_request(self) -> str:
        """
        Возвращает содержимое строки поиска.
        """
        return self.searching_edit.text()

    def _handle_text_changing(self) -> None:
        """
        Обрабатывает обновление строки поиска.
        """
        self._redraw()

    def _clear(self) -> None:
        """
        Очищает виджет.
        """
        self.items.clear()

    def _fast_push(self, widget: QWidget) -> None:
        """
        Быстрое добавление виджета.
        :param widget: Добавляемый виджет.
        """
        item = QListWidgetItem(self.items)
        item.setSizeHint(widget.sizeHint())
        self.items.setItemWidget(item, widget)

    def _add_separator(self, title: str) -> None:
        """
        Добавляет на виджет разделитель.
        :param title: Заголовок разделителя.
        """
        widget = ListSeparatorWidget(title)
        self._fast_push(widget)

    def _add_searching_result(self, major: str, minor: str, callback: Callable) -> None:
        """
        Добавляет на виджет результат поиска.
        :param major: Главная информация.
        :param minor: Дополнительная информация.
        :param callback: Функция-реакция на нажатие.
        """
        widget = SearchingResultWidget(major, minor, callback)
        self._fast_push(widget)

    def _get_filtered_notes_by_name(self) -> List[Tuple[NoteData, str]]:
        """
        Возвращает список результатов по имени.
        """
        groups = self._sql_groups_user.get_groups_dict()
        request = self._get_request()
        if not self._get_regex_using():
            return [(note, groups[note.group].name)
                    for note in self._sql_notes_user.get_all_notes() if is_sub_sequence(note.name.lower(),
                                                                                        request.lower())]

    def _get_filtered_notes_by_text(self) -> List[Tuple[NoteData, int]]:
        """
        Возвращает список результатов поиска по содержимому.
        """
        notes = self._sql_notes_user.get_all_notes()
        request = self._get_request()
        if self._get_regex_using():
            try:
                return [(note, next(re.finditer(request, note.text.lower())).start())
                        for note in notes if re.findall(request, note.text.lower())]
            except re.error:
                return []
        else:
            return [(note, note.text.lower().find(request.lower()))
                    for note in notes if is_sub_sequence(note.text.lower(), request.lower())]

    def _get_filtered_notes_by_tags(self) -> List[NoteWithTags]:
        """
        Возвращает список результатов поиска по тегам.
        """
        notes = self._sql_notes_user.get_all_notes()
        notes = list(zip(notes, [self._sql_tags_user.get_all_tags_by_note_id(note.id) for note in notes]))
        request = set(self._get_request().split())
        return [NoteWithTags(note, tags) for note, tags in notes if request & set(tags)]

    def _get_filtered_groups_by_name(self) -> List[GroupData]:
        """
        Возвращает список результатов поиска по имени.
        """
        groups = self._sql_groups_user.get_all_groups()
        request = self._get_request()
        if not self._get_regex_using():
            return [group for group in groups if is_sub_sequence(group.name.lower(), request.lower())]

    def _redraw(self) -> None:
        """
        Очищает виджет и рисует результаты поиска.
        """
        self._clear()
        notes_by_name = self._get_filtered_notes_by_name()
        notes_by_text = self._get_filtered_notes_by_text()
        notes_by_tags = self._get_filtered_notes_by_tags()
        groups_by_name = self._get_filtered_groups_by_name()
        if not (notes_by_name or notes_by_text or notes_by_tags or groups_by_name):
            self._add_separator('Ничего не найдено :(')
            return

        if notes_by_name:
            self._add_separator('Заметки')
            for note, group_name in notes_by_name:
                self._add_searching_result(note.name,
                                           f'{group_name} - {note.creation_date.strftime(consts.DATETIME_FORMAT)}',
                                           construct_function_with_args(self.note_chosen.emit,
                                                                        note.id,
                                                                        0))
        if groups_by_name:
            self._add_separator('Группы')
            for group in groups_by_name:
                self._add_searching_result(group.name,
                                           '',
                                           construct_function_with_args(self.group_chosen.emit,
                                                                        group.id))
        if notes_by_tags:
            self._add_separator('Результаты по тегам')
            for note in notes_by_tags:
                self._add_searching_result(note.data.name,
                                           '; '.join(note.tags),
                                           construct_function_with_args(self.note_chosen.emit,
                                                                        note.data.id,
                                                                        0))
        if notes_by_text:
            self._add_separator('Результаты по тексту')
            for note, position in notes_by_text:
                self._add_searching_result(f'{note.name} - {note.creation_date.strftime(consts.DATETIME_FORMAT)}',
                                           note.text[position:position + POSITION_SLICE],
                                           construct_function_with_args(self.note_chosen.emit,
                                                                        note.id,
                                                                        position))
