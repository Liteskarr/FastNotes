import PyQt5.uic as uic
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtWidgets import (QWidget)

from structures.notice import NoticeData


class NoticeItemWidget(QWidget):
    note_chosen = pyqtSignal(int)
    notice_dropped = pyqtSignal(int)

    def __init__(self, data: NoticeData):
        super().__init__()
        self._data = data
        self._configure_ui()

    def _configure_ui(self):
        uic.loadUi('uics/notice_item.ui', self)
        self.link_button.clicked.connect(lambda: self.note_chosen.emit(self._data.note))
        self.drop_button.clicked.connect(lambda: self.notice_dropped.emit(self._data.id))
        self.date_label.setText(self._data.date.strftime("%d.%m.%Y %H:%M"))
        self.description_text.setPlainText(self._data.description)
