"""
Модуль, отвечающий за отображение результата поиска в QListWidget.
"""

from typing import Callable

import PyQt5.uic as uic
from PyQt5.QtCore import (QObject, QEvent)
from PyQt5.QtWidgets import (QWidget)


def fizzbuzz() -> None:
    pass


class SearchingResultWidget(QWidget):
    def __init__(self,
                 major: str = '',
                 minor: str = '',
                 clicked_callback: Callable = fizzbuzz):
        super().__init__()
        self._major = major
        self._minor = minor
        self._clicked_callback = clicked_callback
        self._configure_ui()

    def _configure_ui(self):
        uic.loadUi('uics/searching_result_panel.ui', self)
        self.major.installEventFilter(self)
        self.minor.installEventFilter(self)
        self.installEventFilter(self)
        self.major.setText(self._major)
        self.minor.setText(self._minor)
        if not self._minor:
            self.minor.setVisible(False)

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.MouseButtonRelease:
            self._clicked_callback()
        return super(SearchingResultWidget, self).eventFilter(source, event)
