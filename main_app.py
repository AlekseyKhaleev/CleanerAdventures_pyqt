import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from source.main_widget import MainWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOverrideCursor(Qt.CursorShape.BlankCursor)

    window = MainWidget()
    window.showFullScreen()

    app.exec()
