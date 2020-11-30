"""
Модуль отвечает за отображение группы заметок в проводнике.
"""


import PyQt5.uic as uic
from PyQt5.QtCore import (Qt, pyqtSignal, QObject, QEvent)
from PyQt5.QtGui import (QMouseEvent)
from PyQt5.QtWidgets import (QWidget,
                             QCheckBox)

from structures.group import GroupData


class GroupItemWidget(QWidget):
    double_clicked = pyqtSignal(int)
    deleted = pyqtSignal(int)
    renamed = pyqtSignal(GroupData)

    def __init__(self, group: GroupData, checkbox: QCheckBox, parent=None):
        super().__init__(parent)
        self._group = group
        self.edit_checker = checkbox
        self._configure_ui()

    def _configure_ui(self):
        uic.loadUi('uics/group_item.ui', self)
        self.title.setText(self._group.name)
        self.title.editingFinished.connect(self._handle_value_changing)
        self.title.selectionChanged.connect(self._selection_filter)
        self.title.installEventFilter(self)
        self.installEventFilter(self)
        self.delete_button.clicked.connect(self._handle_deleting)
        self.edit_checker.clicked.connect(self._swap_mode)

    def _swap_mode(self) -> None:
        self.title.setReadOnly(not self.edit_checker.checkState())

    def _selection_filter(self) -> None:
        if not self.edit_checker.checkState():
            self.title.deselect()

    def _handle_value_changing(self) -> None:
        self._group.name = self.title.text()
        self.renamed.emit(self._group)

    def _handle_deleting(self) -> None:
        self.deleted.emit(self._group.id)

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.MouseButtonDblClick and not self.edit_checker.checkState():
            self.double_clicked.emit(self._group.id)
        return super(GroupItemWidget, self).eventFilter(source, event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.double_clicked.emit(self._group.id)
