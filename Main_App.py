from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt

import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOverrideCursor(Qt.CursorShape.BlankCursor)

    window = QMainWindow()
    window.showFullScreen()

    app.exec()
