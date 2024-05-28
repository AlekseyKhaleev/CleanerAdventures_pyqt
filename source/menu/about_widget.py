from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel

from source.menu.menu_widget import Menu


class AboutWidget(QWidget):
    # signals
    returnClicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        title = QLabel("About Cleaner Adventures")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("QLabel { font: bold; font-size: 72px }")
        about_label = QLabel()
        about_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        about_label.setStyleSheet("QLabel { font: bold; font-size: 32px }")
        about_label.setText(
            "Python/PyQt open source project\n"
            "created by Aleksey Khaleev\n\n"
            "CleanerAdventures: A game about a robotic vacuum cleaner's adventures in dynamically generated mazes.\n\n"
            "Features:\n"
            "- Dynamically generated mazes with increasing complexity.\n"
            "- Multiple paths to solve mazes.\n"
            "- Energy restoration mechanics.\n\n"
            "Version 1.0\n\n"
            "GitHub Repository: https://github.com/AlekseyKhaleev/CleanerAdventures_pyqt.git"
        )

        layout.addWidget(title, 0, 0, 1, 1)
        layout.addWidget(about_label, 1, 0, 4, 1)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.returnClicked.emit(Menu.RETURN)
