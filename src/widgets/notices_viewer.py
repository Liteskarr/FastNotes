"""
Модуль, отвечающий за отрисовку всех существующих напоминаний.
Самостоятельно выполняет SQL-запросы, однако требует внешнего подключения к БД.
"""

import sqlite3

import PyQt5.uic as uic
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtWidgets import (QDialog,
                             QWidget,
                             QListWidgetItem)

from src.dbuser.notice import NoticeUser
from src.structures.notice import NoticeData
from src.widgets.notice_item import NoticeItemWidget


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
        """
        Быстрое добавление виджета.
        :param widget: Добавляемый виджет.
        """
        item = QListWidgetItem(self.notices)
        item.setSizeHint(widget.sizeHint())
        self.notices.setItemWidget(item, widget)

    def _handle_notice_drop(self, notice_id: int) -> None:
        """
        Обрабатывает прочтение уведомления.
        :param notice_id: ID уведомления.
        """
        self.notice_dropped.emit(notice_id)
        self._redraw()

    def _handle_note_chosen(self, note_id: int) -> None:
        """
        Обрабатывает переход к заметке.
        :param note_id: ID заметки.
        """
        self.note_chosen.emit(note_id, 0)
        self.close()

    def _draw_notice(self, data: NoticeData) -> None:
        """
        Рисует на виджет уведомление по его данным.
        :param data: Данные уведомления.
        """
        widget = NoticeItemWidget(data=data)
        widget.note_chosen.connect(self._handle_note_chosen)
        widget.notice_dropped.connect(self._handle_notice_drop)
        self._fast_push(widget)

    def _clear(self) -> None:
        """
        Очищает виджет.
        """
        self.notices.clear()

    def _redraw(self) -> None:
        """
        Очищает виджет и после рисует все уведомления.
        """
        self._clear()
        notices = self._sql_notices_user.get_unread_notices_ordered_by_date()
        for notice in notices:
            self._draw_notice(notice)
