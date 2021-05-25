"""
Диалоговое окно справки.
"""

import PyQt5.uic as uic
# Из-за особенностей PyQt строку ниже удалять не требуется
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (QDialog,
                             QWidget)


class HelpPanelWidget(QDialog):
    def __init__(self, parent: QWidget, html: str):
        super().__init__(parent)
        self._html = html
        self._configure_ui()

    def _configure_ui(self):
        uic.loadUi('uics/help.ui', self)
        self.web_view.setHtml(self._html)
