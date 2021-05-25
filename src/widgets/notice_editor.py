"""
Модуль, отвечающий за создание напоминания на заметку.
"""

from datetime import datetime

import PyQt5.uic as uic
from PyQt5.QtCore import (pyqtSignal,
                          QDateTime)
from PyQt5.QtWidgets import (QDialog,
                             QWidget)

from src.structures.note import NoteData
from src.structures.notice import NoticeData


class NoticeEditorWidget(QDialog):
    notice_added = pyqtSignal(NoticeData)

    def __init__(self, parent: QWidget, note: NoteData):
        super().__init__(parent)
        self._note = note
        self._configure_ui()

    def _configure_ui(self):
        uic.loadUi('uics/notice_editor.ui', self)
        now_dt = datetime.now()
        self.add_button.clicked.connect(self._handle_adding)
        self.cancel_button.connect(self._handle_closing)
        self.date_editor.setMinimumDateTime(QDateTime(now_dt.year,
                                                      now_dt.month,
                                                      now_dt.day,
                                                      now_dt.hour,
                                                      now_dt.minute))

    def _handle_adding(self) -> None:
        """
        Обрабатывает добавление уведомления.
        """
        notice = NoticeData(id=0,
                            note=self._note,
                            description=self.description_editor.toPlainText(),
                            date=self.date_editor.dateTime().toPyDateTime())
        self.notice_added.emit(notice)
        self.close()

    def _handle_closing(self) -> None:
        """
        Обрабатывает закрытие редактора.
        """
        self.close()
