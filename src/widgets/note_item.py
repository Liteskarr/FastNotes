"""
Модуль, отвечающий за отображение заметки в проводнике.
"""

from typing import List

import PyQt5.uic as uic
from PyQt5.QtCore import (pyqtSignal, QObject, QEvent)
from PyQt5.QtWidgets import (QWidget)

from src.structures.note import NoteData


class NoteItemWidget(QWidget):
    clicked = pyqtSignal(int)

    def __init__(self, data: NoteData, tags: List[str] = None, parent=None):
        super().__init__(parent)
        self._data = data if data is not None else NoteData()
        self._tags = tags if tags is not None else []
        self._configure_ui()

    def _configure_ui(self):
        uic.loadUi('uics/note_item.ui', self)
        self.installEventFilter(self)
        self.tags.setText('; '.join(self._tags)) if self._tags else self.tags.setText('')
        self.tags.installEventFilter(self)
        self.title.installEventFilter(self)
        self.title.setText(self._data.name)
        self.date.installEventFilter(self)
        self.date.setText(self._data.creation_date.strftime('%d.%m.%Y'))

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.MouseButtonPress:
            self.clicked.emit(self._data.id)
            return True
        return super(NoteItemWidget, self).eventFilter(source, event)
