from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from menu_widget import Menu


class AboutWidget(QWidget):
    # signals
    returnClicked = pyqtSignal(int)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        layout = QGridLayout()
        title = QLabel("About Cleaner Adventures")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("QLabel { font: bold; font-size: 72px }")
        about_label = QLabel()
        about_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        about_label.setStyleSheet("QLabel { font: bold; font-size: 32px }")
        about_label.setText("Qt 6.4/C++ open source project\n"
                            "created by Aleksey Khaleev 27.12.2022\n\n\n"
                            "NIZHNY NOVGOROD STATE TECHNICAL UNIVERSITY\n"
                            "Institute of Radioelectronics and Information Technologies\n"
                            "Department of Informatics and Control Systems\n\n"
                            "Programming course work\n\n"
                            "\"Modelling the operation of a finite state machine\"\n\n"
                            "version 1.0\n\n\n"
                            "https://github.com/AlekseyKhaleev/CleanerAdventures.git")
        layout.addWidget(title, 0, 0, 1, 1)
        layout.addWidget(about_label, 1, 0, 4, 1)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.returnClicked.emit(Menu.RETURN)
