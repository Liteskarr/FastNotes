import sqlite3
from typing import List

import PyQt5.uic as uic
from PyQt5.QtWidgets import (QMainWindow,
                             QMessageBox)

from widgets.explorer import ExplorerWidget
from widgets.note_editor import NoteEditorWidget
from widgets.searching_dialog import SearchingDialog
from widgets.tags_editor import TagsEditorWidget
from widgets.help_panel import HelpPanelWidget
from widgets.notice_editor import NoticeEditorWidget
from widgets.notices_viewer import NoticesViewWidget

from structures.notice import NoticeData
from structures.note import NoteData
from structures.group import GroupData
from structures.tags_update import TagsUpdate
from structures.note_with_tags import NoteWithTags

from dbuser.note import NotesUser
from dbuser.group import GroupsUser
from dbuser.tag import TagUser
from dbuser.notice import NoticeUser


class Window(QMainWindow):
    def __init__(self, dbname: str, header: str):
        super().__init__()
        self._dbname = dbname
        self._header = header
        self._init_sql()
        self._configure_ui()
        self._swap_explorer_visible()
        self._draw_groups()

    def _init_sql(self):
        self._connection = sqlite3.connect(self._dbname)
        self._sql_notes_user = NotesUser()
        self._sql_groups_user = GroupsUser()
        self._sql_tags_user = TagUser()
        self._sql_notice_user = NoticeUser()
        self._sql_notes_user.set_connection(self._connection)
        self._sql_groups_user.set_connection(self._connection)
        self._sql_tags_user.set_connection(self._connection)
        self._sql_notice_user.set_connection(self._connection)

    def _init_users_widgets(self):
        self.explorer_widget = ExplorerWidget()
        self.explorer_widget.note_chosen.connect(self._handle_note_choosing)
        self.explorer_widget.note_added.connect(self._handle_note_adding)
        self.explorer_widget.group_chosen.connect(self._handle_group_choosing)
        self.explorer_widget.group_added.connect(self._handle_group_adding)
        self.explorer_widget.group_closed.connect(self._handle_group_closing)
        self.explorer_widget.group_renamed.connect(self._handle_group_renaming)
        self.explorer_widget.group_deleted.connect(self._handle_group_deleting)
        self.explorer_widget.info_button_clicked.connect(self._handle_info_button_click)
        self.explorer_widget.searching_button_clicked.connect(self._handle_searching_button_click)
        self.explorer_widget.notices_button_clicked.connect(self._handle_notices_opening)
        self.main_layout.addWidget(self.explorer_widget)

        self.note_widget = NoteEditorWidget()
        self.note_widget.set_header(self._header)
        self.note_widget.saved.connect(self._handle_note_saving)
        self.note_widget.closed.connect(self._handle_note_closing)
        self.note_widget.deleted.connect(self._handle_note_deleting)
        self.note_widget.tags_button_clicked.connect(self._handle_tag_editor)
        self.note_widget.notice_button_clicked.connect(self._handle_notice_editor_opening)
        self.main_layout.addWidget(self.note_widget)

    def _configure_ui(self):
        uic.loadUi('uics/window.ui', self)
        self._init_users_widgets()
        self.menu_button.clicked.connect(self._swap_explorer_visible)

    def _swap_explorer_visible(self) -> None:
        visible = self.explorer_widget.isVisible()
        self.explorer_widget.setVisible(not visible)
        self.menu_button.setText('<' if not visible else '>')

    def _fix_explorer(self):
        self.explorer_widget.items.adjustSize()

    def _handle_note_adding(self, group_id: int) -> None:
        self._sql_notes_user.create_new_note('Новая заметка...', group_id)
        self._sql_notes_user.commit()
        self._draw_group(group_id)

    def _handle_note_deleting(self, data: NoteData) -> None:
        status = QMessageBox.question(self,
                                      'Удаление заметки',
                                      'Вы уверены, что желаете это сделать? Отмена невозможна.',
                                      QMessageBox.Yes | QMessageBox.No)
        if status == QMessageBox.Yes:
            self.note_widget.drop_data()
            self._sql_notes_user.delete_note_by_id(data.id)
            self._sql_notes_user.commit()
            self._draw_group(data.group)

    def _handle_note_saving(self, data: NoteData) -> None:
        self._sql_notes_user.update_note_data(data)
        self._sql_notes_user.commit()
        self._draw_group(data.group)

    def _handle_note_closing(self) -> None:
        if self.note_widget.get_data() is not None and self.note_widget.is_not_saved():
            answer = QMessageBox.question(self,
                                          'Перемога!',
                                          'Сохранить изменения?',
                                          QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                self.note_widget.save()
        self._draw_group(self.note_widget.get_data().group)
        self.note_widget.drop_data()

    def _handle_note_choosing(self, note_id: int, cursor_position: int = 0) -> None:
        if self.note_widget.get_data() is not None and self.note_widget.get_data().id == note_id:
            return
        if self.note_widget.get_data() is not None and self.note_widget.is_not_saved():
            answer = QMessageBox.question(self,
                                          'Перемога!',
                                          'Сохранить изменения?',
                                          QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                self.note_widget.save()
        note = self._sql_notes_user.get_note_by_id(note_id)
        self.note_widget.set_data(note)
        self.note_widget.set_editing_field_cursor_position(cursor_position)
        self._draw_group(note.group)

    def _handle_group_adding(self) -> None:
        self._sql_groups_user.create_new_group('Новая группа')
        self._sql_groups_user.commit()
        self._draw_groups()

    def _handle_group_renaming(self, group: GroupData) -> None:
        self._sql_groups_user.update_group_name(group.id, group.name)
        self._sql_groups_user.commit()

    def _handle_group_deleting(self, group_id: int) -> None:
        status = QMessageBox.question(self,
                                      'Удаление группы заметок',
                                      'Вы уверены? Данное действие невозможно отменить!',
                                      QMessageBox.Yes | QMessageBox.No)
        if status == QMessageBox.Yes:
            self._sql_notes_user.delete_notes_by_group_id(group_id)
            self._sql_groups_user.delete_group_by_id(group_id)
            self._sql_tags_user.disconnect_tags_by_group_id(group_id)
            self._sql_notes_user.commit()
            self._sql_groups_user.commit()
            self._sql_tags_user.commit()
            self._draw_groups()
            if self.note_widget.get_data() is not None and self.note_widget.get_data().group == group_id:
                self.note_widget.drop_data()

    def _handle_group_closing(self) -> None:
        if self.note_widget.get_data() is not None and self.note_widget.is_not_saved():
            self._handle_note_closing()
        self._draw_groups()

    def _handle_group_choosing(self, group_id: int) -> None:
        self._draw_group(group_id)

    def _handle_searching_button_click(self) -> None:
        dialog = SearchingDialog(self, self._connection)
        dialog.note_chosen.connect(self._handle_note_choosing)
        dialog.group_chosen.connect(self._handle_group_choosing)
        dialog.show()

    def _handle_tags_saving(self, update: TagsUpdate) -> None:
        self._sql_tags_user.connect_tags_with_note_by_id(update.note_id, update.added)
        self._sql_tags_user.disconnect_tags_by_names_and_note_id(update.note_id, update.deleted)
        self._sql_tags_user.commit()
        self._draw_group(self.explorer_widget.current_group_id)

    def _handle_tag_editor(self, note: NoteData) -> None:
        tags = self._sql_tags_user.get_all_tags_by_note_id(note.id)
        tags_editor = TagsEditorWidget(self, note.id, tags)
        tags_editor.saved.connect(self._handle_tags_saving)
        tags_editor.show()

    def _handle_info_button_click(self) -> None:
        HelpPanelWidget(self, ''.join(open('res/help.html', 'r', encoding='utf-8'))).show()

    def _handle_notice_drop(self, notice_id: int) -> None:
        self._sql_notice_user.read_notice(notice_id)
        self._sql_notice_user.commit()

    def _handle_notice_editor_opening(self, note: NoteData) -> None:
        notice_editor = NoticeEditorWidget(self, note)
        notice_editor.notice_added.connect(self._handle_notice_adding)
        notice_editor.show()

    def _handle_notice_adding(self, notice: NoticeData) -> None:
        self._sql_notice_user.add_notice(notice)
        self._sql_notice_user.commit()

    def _handle_notices_opening(self) -> None:
        notice_viewer = NoticesViewWidget(self, self._connection)
        notice_viewer.note_chosen.connect(self._handle_note_choosing)
        notice_viewer.notice_dropped.connect(self._handle_notice_drop)
        notice_viewer.show()

    def _draw_group(self, group_id,
                    group: GroupData = None,
                    notes: List[NoteData] = None) -> None:
        group = self._sql_groups_user.get_group_by_id(group_id) if group is None else group
        notes = self._sql_notes_user.get_notes_by_group(group_id) if notes is None else notes
        self.explorer_widget.draw_group(group, [NoteWithTags(note,
                                                             self._sql_tags_user.get_all_tags_by_note_id(note.id))
                                                for note in notes])

    def _draw_groups(self) -> None:
        groups = self._sql_groups_user.get_all_groups()
        self.explorer_widget.draw_groups(groups)
