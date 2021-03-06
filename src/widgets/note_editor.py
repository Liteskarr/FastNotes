"""
Модуль, отвечающий за все взаимодействия пользователя с содержимым заметок, тегами и напоминаниями.
Выполняет подготову данных заметки для зранения в базе данных.
"""

from copy import copy
from datetime import datetime
from itertools import cycle
from typing import Union, List

import PyQt5.uic as uic
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtGui import QTextCursor
# Из-за особенностей PyQt строку ниже удалять не требуется
# noinspection PyUnresolvedReferences
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (QWidget,
                             QFileDialog,
                             QMessageBox)

import src.consts as consts
from src.compiller import precompile, assemble
from src.structures.note import NoteData
from src.structures.notice import NoticeData

VIEW_MODE = 0
EDITING_MODE = 1


class NoteEditorWidget(QWidget):
    saved = pyqtSignal(NoteData)
    deleted = pyqtSignal(NoteData)
    closed = pyqtSignal()

    tags_button_clicked = pyqtSignal(NoteData)
    notice_button_clicked = pyqtSignal(NoteData)

    _MODES_RING = cycle([VIEW_MODE, EDITING_MODE])

    def __init__(self, parent=None):
        super().__init__(parent)
        self._mode: int = 0
        self._data: Union[NoteData, None] = None
        self._notice: Union[NoticeData, None] = None
        self._header: str = ''
        self._configure_ui()
        self._next_mode()
        self.setEnabled(False)

    def _configure_ui(self):
        uic.loadUi('uics/note_editor.ui', self)
        self.title.textChanged.connect(self._handle_editing)
        self.save_button.clicked.connect(self.save)
        self.close_button.clicked.connect(self._handle_closing)
        self.edit_field.textChanged.connect(self._handle_editing)
        self.delete_button.clicked.connect(self._handle_deleting)
        self.mode_button.clicked.connect(self._next_mode)
        self.export_button.clicked.connect(self._export_to_file)
        self.tags_button.clicked.connect(lambda: self.tags_button_clicked.emit(self.get_data()))
        self.notice_button.clicked.connect(lambda: self.notice_button_clicked.emit(self.get_data()))
        self.web_view.hide()
        self.line.hide()

    def _export_to_file(self) -> None:
        """
        Экспортирует заметку в файл.
        """
        self.save()
        filepath = QFileDialog.getSaveFileName(self, 'Выберите файл')[0]
        try:
            file = open(filepath, mode='w', encoding='utf-8')
            file.write(assemble(self._header, precompile(self.edit_field.toPlainText())))
        except Exception:
            QMessageBox.critical(self, 'Ошибка!', 'Ошибка при чтении файла! Попробуйте еще раз!')

    def _reload_web_view(self) -> None:
        """
        Обновляет окно просмотра заметки.
        """
        markdown_text = precompile(self.edit_field.toPlainText())
        self.web_view.setHtml(assemble(self._header, markdown_text))

    def _change_saving_button_bg(self) -> None:
        """
        Обновляет задний фон для кнопки сохранения в зависимости от наличия изменений.
        """
        if self.is_not_saved():
            self.save_button.setStyleSheet('background-color: rgb(0, 85, 255);')
        else:
            self.save_button.setStyleSheet('background-color: rgb(255, 255, 255);')

    def _reload_ui(self) -> None:
        """
        Перезагружает визуальную часть виджета.
        """
        self.line.show()
        self.editing_time_label.setText(self._data.editing_date.strftime(consts.DATETIME_SHOWING_FORMAT))
        self.title.setText(self._data.name)
        self.edit_field.setPlainText(self._data.text)
        self._reload_web_view()
        self._change_saving_button_bg()

    def _next_mode(self) -> None:
        """
        Переключает режим взаимодействия заметки.
        Существует 2 режима: редактирование и просмотр.
        """
        self._mode = next(self._MODES_RING)
        self.pages.setCurrentIndex(self._mode)
        self.title.setReadOnly(self._mode == VIEW_MODE)

    def _handle_closing(self) -> None:
        """
        Обрабатывает закрытие заметки.
        """
        self.closed.emit()

    def _load(self, data: NoteData) -> None:
        """
        Загружает в виджет данных заметки.
        :param data: Данные заметки.
        """
        self.web_view.show()
        self._data = data
        self._data_for_saving = copy(self._data)
        self._reload_ui()

    def _handle_editing(self) -> None:
        """
        Обрабатывает редактирование заметки.
        """
        self._commit()
        self._reload_web_view()
        self._change_saving_button_bg()

    def _commit(self) -> None:
        """
        Сохраняет изменения заметки в буффер сохранения.
        """
        self._data_for_saving.name = self.title.text()
        self._data_for_saving.text = self.edit_field.toPlainText()
        self._data_for_saving.editing_date = datetime.now()

    def save(self) -> None:
        """
        Сохраняет изменения в заметке.
        """
        self.saved.emit(self._data_for_saving)
        self._data = self._data_for_saving
        self._change_saving_button_bg()
        self._reload_ui()

    def _handle_deleting(self) -> None:
        """
        Обрабатывает удаление заметки.
        """
        self.deleted.emit(self._data)

    def drop_data(self) -> None:
        """
        Очищает редактор от данных заметки.
        """
        self.setEnabled(False)
        self.line.hide()
        self.edit_field.clear()
        self.title.clear()
        self.editing_time_label.clear()
        self.save_button.setStyleSheet('background-color: rgb(255, 255, 255);')
        self._data = self._data_for_saving = None
        if self._mode != VIEW_MODE:
            self._next_mode()

    def set_editing_field_cursor_position(self, position: int) -> None:
        """
        Устанавливает позицию курсора в поле редактирования.
        :param position: Позиция курсора.
        """
        cursor = self.edit_field.textCursor()
        cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, position)
        self.edit_field.setTextCursor(cursor)

    def set_header(self, header: str) -> None:
        """
        Устанавливает заголовок заметки.
        :param header: Заголовок.
        """
        self._header = header

    def get_header(self) -> str:
        """
        Возвращает заголовок заметки.
        """
        return self._header

    def set_data(self, data: NoteData) -> None:
        """
        Устанавливает данные заметки.
        :param data: Данные заметки.
        """
        self.setEnabled(True)
        self._load(data)
        self._reload_ui()

    def get_data(self) -> NoteData:
        """
        Возвращает данные заметки.
        """
        return self._data

    def set_tags(self, tags: List[str]) -> None:
        """
        Устанавливает список тегов текущей заметки.
        :param tags: Список тегов.
        """
        self._tags = tags

    def get_tags(self) -> List[str]:
        """
        Возвращает список тегов, которые в данный момент находятся на заметке.
        """
        return self._tags

    def is_not_saved(self) -> bool:
        """
        Возвращает True, если заметка не была сохранена, иначе False.
        """
        return self._data.name != self._data_for_saving.name or self._data.text != self._data_for_saving.text
