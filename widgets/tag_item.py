import PyQt5.uic as uic
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtWidgets import (QWidget)


class TagItem(QWidget):
    deleted = pyqtSignal(str)

    def __init__(self, tag: str):
        super().__init__()
        self._tag = tag
        self._configure_ui()

    def _configure_ui(self):
        uic.loadUi('uics/tag_item.ui', self)
        self.tag_name.setText(self._tag)
        self.deleting_button.clicked.connect(self._handle_tag_deleting)

    def _handle_tag_deleting(self):
        self.deleted.emit(self._tag)
