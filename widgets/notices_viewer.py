import sqlite3

import PyQt5.uic as uic
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtWidgets import (QDialog,
                             QWidget,
                             QListWidgetItem)

from dbuser.notice import NoticeUser
from structures.notice import NoticeData
from widgets.notice_item import NoticeItemWidget


class NoticesViewWidget(QDialog):
    notice_dropped = pyqtSignal(int)
    note_chosen = pyqtSignal(int, int)

    def __init__(self, parent: QWidget, connection: sqlite3.Connection):
        super().__init__(parent)
        self._sql_notices_user = NoticeUser()
        self._sql_notices_user.set_connection(connection)
        self._configure_ui()
        self._redraw()

    def _configure_ui(self):
        uic.loadUi('uics/notices_viewer.ui', self)

    def _fast_push(self, widget: QWidget) -> None:
        item = QListWidgetItem(self.notices)
        item.setSizeHint(widget.sizeHint())
        self.notices.setItemWidget(item, widget)

    def _handle_notice_drop(self, notice_id: int) -> None:
        self.notice_dropped.emit(notice_id)
        self._redraw()

    def _handle_note_chosen(self, note_id: int) -> None:
        self.note_chosen.emit(note_id, 0)
        self.close()

    def _draw_notice(self, data: NoticeData):
        widget = NoticeItemWidget(data=data)
        widget.note_chosen.connect(self._handle_note_chosen)
        widget.notice_dropped.connect(self._handle_notice_drop)
        self._fast_push(widget)

    def _clear(self):
        self.notices.clear()

    def _redraw(self):
        self._clear()
        notices = self._sql_notices_user.get_unread_notices_ordered_by_date()
        for notice in notices:
            self._draw_notice(notice)
