import PyQt5.uic as uic
from PyQt5.QtCore import (Qt, pyqtSignal, QObject, QEvent)
from PyQt5.QtGui import (QMouseEvent)
from PyQt5.QtWidgets import (QWidget,
                             QCheckBox)

from structures.group import GroupData


class GroupItem(QWidget):
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
        self.title.editingFinished.connect(self._value_changed_handler)
        self.title.selectionChanged.connect(self._selection_filter)
        self.title.installEventFilter(self)
        self.installEventFilter(self)
        self.delete_button.clicked.connect(self._delete_handler)
        self.edit_checker.clicked.connect(self._swap_mode)

    def _swap_mode(self):
        self.title.setReadOnly(not self.edit_checker.checkState())

    def _selection_filter(self):
        if not self.edit_checker.checkState():
            self.title.deselect()

    def _value_changed_handler(self):
        self._group.name = self.title.text()
        self.renamed.emit(self._group)

    def _delete_handler(self):
        self.deleted.emit(self._group.id)

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.MouseButtonDblClick and not self.edit_checker.checkState():
            self.double_clicked.emit(self._group.id)
        return super(GroupItem, self).eventFilter(source, event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.double_clicked.emit(self._group.id)
