from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from MainWidget import MainWidget

import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOverrideCursor(Qt.CursorShape.BlankCursor)

    window = MainWidget()
    window.showFullScreen()

    app.exec()
