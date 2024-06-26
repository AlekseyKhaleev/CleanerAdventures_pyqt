from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit


class AuthWidget(QWidget):
    # signals
    nameChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__layout = QVBoxLayout()
        self.__auth = QLineEdit()
        self.__auth.returnPressed.connect(self.__change_name)
        auth_label = QLabel("Enter your name, robot: ")
        auth_label.setStyleSheet("font: bold; font-size: 72px; color: white; background-color: black")
        self.__auth.setMaxLength(12)
        self.__auth.setStyleSheet("border: 6px solid white; border-radius: 30px; font: bold; font-size: 48px; "
                                  "color: white; background-color: black; width: 360px")
        self.__auth.setTextMargins(12, 0, 0, 0)

        self.__layout.addWidget(auth_label, 1, Qt.AlignmentFlag.AlignCenter)
        self.__layout.addWidget(self.__auth, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self.__layout)

    # slots
    def __change_name(self):
        self.nameChanged.emit(self.__auth.text())
        self.__auth.clear()
