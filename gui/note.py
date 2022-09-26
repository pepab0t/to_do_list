from datetime import datetime
from typing import Any, Optional

from config import PATH, date_format
from events import Events
from pydantic import BaseModel, Field, validator
from PySide2 import QtGui, QtWidgets

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
        self.event_handler.title(value)
        self.content = value

    @property
    def created_p(self):
        return self.created.strftime(date_format)

    @property
    def deadline_p(self):
        if not self.deadline:
            return None
        return self.deadline.strftime(date_format)

    @deadline_p.setter
    def deadline_p(self, value: datetime):
        """When value set for deadline_set, appropriated event called"""
        self.event_handler.deadline(value)
        self.deadline = value

    class Config:
        arbitrary_types_allowed = True

class Note(QtWidgets.QFrame):
    def __init__(self, data: dict[str, Any], parent=None):
        super().__init__(parent)
        UiLoader().loadUi(f"{PATH}/gui/note.ui", self)

        self.data: NoteData = NoteData(**data)

        self.labelTitle.setText(self.data.title_p)
        self.editContent.setText(self.data.content_p)
        self.labelCreated.setText(self.data.created_p)
        self.labelDeadline.setText(self.data.deadline_p)

        self.data.event_handler.title += self.labelTitle.setText  # type: ignore
        self.data.event_handler.content += self.editContent.setText  # type: ignore
        self.data.event_handler.deadline += self.labelDeadline.setText  # type: ignore
