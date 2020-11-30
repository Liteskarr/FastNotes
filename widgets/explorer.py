"""
Модуль, берущий на себя ответственность за навигацию по группам и заметкам.
Также через него осуществляется переход на диалоговые окна напоминаний и поиска.
Упоминается в документации, как проводник.
"""


from typing import List, Callable

import PyQt5.uic as uic
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtWidgets import (QWidget,
                             QListWidget,
                             QListWidgetItem, QPushButton)

from structures.group import GroupData
from structures.note import NoteData
from structures.note_with_tags import NoteWithTags
from widgets.group_item import GroupItemWidget
from widgets.list_separator import ListSeparatorWidget
from widgets.note_item import NoteItemWidget


class ExplorerWidget(QWidget):
    note_chosen = pyqtSignal(int)
    note_added = pyqtSignal(int)

    group_chosen = pyqtSignal(int)
    group_renamed = pyqtSignal(GroupData)
    group_deleted = pyqtSignal(int)
    group_closed = pyqtSignal()
    group_added = pyqtSignal()

    searching_button_clicked = pyqtSignal()
    info_button_clicked = pyqtSignal()
    notices_button_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.current_group_id = -1
        self._configure_ui()

    def _configure_ui(self):
        self.items: QListWidget
        uic.loadUi('uics/explorer.ui', self)
        self.info_button.clicked.connect(self.info_button_clicked.emit)
        self.searching_button.clicked.connect(self.searching_button_clicked.emit)
        self.notices_button.clicked.connect(self.notices_button_clicked.emit)

    def _handle_group_deleted(self, group_id: int):
        self.group_deleted.emit(group_id)

    def _handle_group_renamed(self, group: GroupData):
        self.group_renamed.emit(group)

    def _handle_group_item_click(self, group_id: int):
        self.group_chosen.emit(group_id)

    def _handle_note_item_click(self, note_id: int):
        self.note_chosen.emit(note_id)

    def _handle_searching_note_taken(self, note_id: int) -> None:
        self.note_chosen.emit(note_id)

    def _handle_searching_start(self):
        self.start_searching.emit(self.search_edit.text(), self.use_regex.checkState())

    def _fast_push(self, widget: QWidget):
        item = QListWidgetItem(self.items)
        item.setSizeHint(widget.sizeHint())
        self.items.setItemWidget(item, widget)

    def _add_button(self, title: str, function: Callable):
        widget = QPushButton()
        widget.setText(title)
        widget.clicked.connect(function)
        self._fast_push(widget)

    def _add_separator(self, title: str = ''):
        widget = ListSeparatorWidget(title)
        self._fast_push(widget)

    def _add_note(self, note: NoteData, tags: List[str]):
        widget = NoteItemWidget(note, tags)
        widget.clicked.connect(lambda: self.note_chosen.emit(note.id))
        self._fast_push(widget)

    def _add_group(self, group: GroupData):
        widget = GroupItemWidget(group, self.edit_checker)
        widget.double_clicked.connect(self._handle_group_item_click)
        widget.renamed.connect(self._handle_group_renamed)
        widget.deleted.connect(self._handle_group_deleted)
        self._fast_push(widget)

    def update_notices_existing(self, notices_exist: bool):
        if notices_exist:
            self.notices_button.setStyleSheet('background-color: rgb(255, 85, 0);')
        else:
            self.notices_button.setStyleSheet('background-color: rgb(255, 255, 255);')

    def clear(self):
        self.items.clear()
        self.edit_checker.setVisible(False)
        self.edit_checker.setChecked(False)

    def draw_groups(self, groups: List[GroupData]):
        self.clear()
        self.current_group_id = -1
        self.edit_checker.setVisible(True)
        for group in groups:
            self._add_group(group)
        self._add_button('+', self.group_added.emit)
        self.items.setMinimumWidth(self.items.sizeHintForColumn(0))

    def draw_group(self, group: GroupData, notes: List[NoteWithTags]):
        self.current_group_id = group.id
        self.clear()
        self._add_button('⮬', self.group_closed.emit)
        self._add_separator(group.name)
        for note in notes:
            self._add_note(note.data, note.tags)
        self._add_button('+', lambda: self.note_added.emit(group.id))
        self.items.setMinimumWidth(self.items.sizeHintForColumn(0))
