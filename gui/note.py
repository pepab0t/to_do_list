import re
from datetime import datetime
from typing import Any, Optional

from config import PATH, DateFormat, date_pattern
from events import Events
from future import __annotations__
from pydantic import BaseModel, Field, validator
from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import Signal

from .loader import UiLoader


class NoteData(BaseModel):
    title: str
    content: str
    deadline: Optional[datetime] = None

    created: datetime = Field(datetime.now())
    event_handler: Events = Field(Events(('title', 'content', 'deadline')))

    # @validator('event_handler')
    # @classmethod
    # def init_exclude_event_handler(cls, v):
    #     return Events(('title', 'content', 'deadline'))

    @validator('created')
    @classmethod
    def init_exclude_created(cls, v):
        return datetime.now()

    @property
    def title_p(self):
        return self.title

    @title_p.setter
    def title_p(self, value: str):
        """When value set for title_set, appropriated event called"""
        self.event_handler.title(value)
        self.title = value

    @property
    def content_p(self):
        return self.content

    @content_p.setter
    def content_p(self, value: str):
        """When value set for content_set, appropriated event called"""
        self.event_handler.content(value)
        self.content = value

    @property
    def created_p(self):
        return self.created.strftime(DateFormat.STANDARD.value)

    @property
    def deadline_p(self):
        if not self.deadline:
            return None
        return self.deadline.strftime(r"%d.%m.%Y")

    @deadline_p.setter
    def deadline_p(self, value: datetime):
        """When value set for deadline_set, appropriated event called"""
        self.event_handler.deadline(value)
        self.deadline = value

    class Config:
        arbitrary_types_allowed = True

class Note(QtWidgets.QFrame):
    state_changed = Signal()
    deleted = Signal(int) # parameter should be Note ID (nid)

    ID: int = 0

    def __init__(self, data: dict[str, Any], parent):
        self.nid = self.ID
        self.increase_ID()
        super().__init__(parent)
        UiLoader().loadUi(f"{PATH}/gui/note.ui", self)

        self.data: Optional[NoteData] = None
        self.labelContent.hide()

        self.buttonConfirm.clicked.connect(self.confirm)
        self.buttonEdit.clicked.connect(self.edit)
        self.buttonDelete.clicked.connect(lambda: self.deleted.emit(self.nid)) # type: ignore # delete
        self.buttonMark.clicked.connect(lambda: self.mark_completed(True))

        # starting at opened state
        self.is_opened: bool = True
        self.completed: bool = False

        # self.editTitle.setText(self.data.title_p)
        # self.editContent.setText(self.data.content_p)
        # self.labelCreated.setText(self.data.created_p)
        # self.editDeadline.setText(self.data.deadline_p)

        # self.data.event_handler.title += self.labelTitle.setText  # type: ignore
        # self.data.event_handler.content += self.editContent.setText  # type: ignore
        # self.data.event_handler.deadline += self.labelDeadline.setText  # type: ignore

    @classmethod
    def increase_ID(cls):
        cls.ID += 1

    # def __repr__(self) -> str:
    #     return f"note ID: {self.nid}"

    def mark_completed(self, state: bool):
        self.completed = state
        self.editTitle.setEnabled(not state)
        self.buttonEdit.setEnabled(not state)
        self.frameBody.setEnabled(not state)
        self.buttonMark.setEnabled(True)
        self.buttonDelete.setEnabled(True)
        self.buttonMark.clicked.disconnect()
        self.buttonMark.clicked.connect(lambda: self.mark_completed(not state))


    def lock(self, state: bool = True):
        self.editTitle.setReadOnly(state)
        self.editDeadline.setReadOnly(state)
        self.editContent.setReadOnly(state)

        self.is_opened = not state

        # self.editTitle.setStyleSheet("QLineEdit[readOnly=\"true\"]{ background-color: rgb(220, 138, 221); }")
        # self.editTitle.setStyleSheet()

        self.editTitle.style().polish(self.editTitle)
        self.editDeadline.style().polish(self.editDeadline)
        self.editContent.style().polish(self.editContent)
        # self.style().polish(self)

        self.state_changed.emit()  # type: ignore

    def validate_date(self, date_input: str) -> Optional[datetime]:

        date_match = date_pattern.match(date_input)
        
        if date_match:
            try:
                args = [int(x) for x in date_match.groups()][::-1]
                return datetime(*args)  # type: ignore
            except ValueError:
                return None
        else:
            return None

    def confirm(self):
        self.lock()

        deadline_input: str = self.editDeadline.text().strip()
        deadline: Optional[datetime] = self.validate_date(deadline_input)

        self.data = NoteData(
            title=self.editTitle.text(),
            content=self.editContent.toPlainText(),
            deadline=deadline
        )  # type: ignore

        self.editDeadline.setText(self.data.deadline_p)
        self.labelCreated.setText(self.data.created_p)
        self.labelContent.setText(self.data.content_p)
        self.labelContent.show()
        self.editContent.hide()
        self.frameConfirm.hide()
    
    def edit(self):
        if self.data:
            self.editContent.setText(self.data.content_p)
        self.editContent.show()
        self.frameConfirm.show()
        self.labelContent.hide()

        self.lock(False)



