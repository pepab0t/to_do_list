from datetime import datetime

from PySide2 import QtCore, QtWidgets

from config import PATH
from gui import loader
from gui.note import Note


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        loader.UiLoader().loadUi(f'{PATH}/gui/gui.ui', self)

        self.notes: list[Note] = []
        self.buttonAdd.clicked.connect(self.addNote)
        self.buttonPrint.clicked.connect(self.print_notes)

    def addNote(self):

        note: Note = Note({
            'title': 'Note 1',
            'content': 'Testing note',
            'deadline': datetime.now()
        }, parent=self.noteFrame)

        note.state_changed.connect(self.manage_status)  # type: ignore
        note.deleted.connect(self.delete_note)  # type: ignore

        self.notes.append(note)
        self.noteLayout.insertWidget(0, note)
        self.manage_status()

    def delete_note(self, note_id: int) -> None:
        for i, note in enumerate(self.notes):
            if note.nid == note_id:
                self.notes.pop(i)
                note.deleteLater()
                break

        # self.manage_status()

    def manage_status(self):
        enabled: bool = all([not x.is_opened for x in self.notes])
        self.buttonAdd.setEnabled(enabled)

        print(self.notes)

        for note in self.notes:
            # try:
            note.buttonEdit.setEnabled(enabled)
            # except RuntimeError:
            #     pass

    def print_notes(self):
        print('---------------')
        for n in self.notes:
            print(f"{n}")
        print('---------------')
        

def main():
    import sys

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app: QtWidgets.QApplication = QtWidgets.QApplication(sys.argv)
    window: MainWindow = MainWindow()

    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
