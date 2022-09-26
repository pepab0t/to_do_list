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

    def addNote(self):

        note: Note = Note({
            'title': 'Note 1',
            'content': 'Testing note',
            'deadline': datetime.now()
        }, parent=self.noteFrame)

        self.notes.append(note)
        self.noteLayout.addWidget(note)

def main():
    import sys

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app: QtWidgets.QApplication = QtWidgets.QApplication(sys.argv)
    window: MainWindow = MainWindow()

    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
