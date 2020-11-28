import PyQt5.uic as uic
from PyQt5.QtWidgets import (QWidget)


class ListSeparatorWidget(QWidget):
    def __init__(self, title: str):
        super().__init__()
        self._title = title
        self._configure_ui()

    def _configure_ui(self):
        uic.loadUi('uics/list_separator.ui', self)
        self.title_label.setText(self._title)
