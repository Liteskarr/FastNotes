from typing import List

import PyQt5.uic as uic
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.QtWidgets import (QDialog,
                             QWidget,
                             QListWidgetItem,
                             QInputDialog)

from widgets.tag_item import TagItem
from structures.tags_update import TagsUpdate


class TagsEditorWidget(QDialog):
    saved = pyqtSignal(TagsUpdate)

    def __init__(self, parent: QWidget, note_id: int, initial_tags: List[str]):
        super().__init__(parent)
        self._tags = [tag.replace("''", "'") for tag in initial_tags]
        self._tags_update = TagsUpdate(note_id)
        self._configure_ui()
        self._redraw()

    def _configure_ui(self):
        uic.loadUi('uics/tags_editor.ui', self)
        self.adding_button.clicked.connect(self._handle_tag_adding)
        self.canceling_button.clicked.connect(self._handle_closing)
        self.saving_button.clicked.connect(self._handle_saving)

    def _draw_tag(self, name: str) -> None:
        widget = TagItem(name)
        widget.deleted.connect(self._handle_tag_deleting)
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        self.tags_list.addItem(item)
        self.tags_list.setItemWidget(item, widget)

    def _add_tag(self, tag: str) -> None:
        if tag in self._tags_update.added or tag in self._tags:
            return
        elif tag in self._tags_update.deleted:
            self._tags_update.deleted.remove(tag)
        else:
            self._tags_update.added.append(tag)
        self._tags.append(tag)

    def _handle_tag_deleting(self, tag: str) -> None:
        if tag in self._tags_update.added:
            self._tags_update.added.remove(tag)
        else:
            self._tags_update.deleted.append(tag)
        self._tags.remove(tag)
        self._redraw()

    def _handle_tag_adding(self) -> None:
        tags, ok_pressed = QInputDialog.getText(self, 'Добавить теги', 'Ввод:')
        if ok_pressed:
            for tag in tags.split():
                self._add_tag(tag)
        self._redraw()

    def _handle_saving(self) -> None:
        self.saved.emit(self._tags_update)
        self._tags_update = TagsUpdate(self._tags_update.note_id)

    def _handle_closing(self) -> None:
        self.close()

    def _clear(self) -> None:
        self.tags_list.clear()

    def _redraw(self) -> None:
        self._clear()
        for tag in self._tags:
            self._draw_tag(tag)
