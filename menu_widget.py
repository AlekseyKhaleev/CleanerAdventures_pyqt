from PyQt6.QtWidgets import QPushButton, QWidget, QLabel, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from dataclasses import dataclass


@dataclass(frozen=True)
class Menu:
    RETURN: int = 0
    NEW_GAME: int = 1
    CONTROLS: int = 2
    HIGHSCORES: int = 3
    ABOUT: int = 4
    EXIT: int = 5
    END_GAME: int = 6


class MenuWidget(QWidget):
    # signals
    returnClicked = pyqtSignal([bool], [int])
    newGameClicked = pyqtSignal([bool], [int])
    controlsClicked = pyqtSignal([bool], [int])
    highscoresClicked = pyqtSignal([bool], [int])
    aboutClicked = pyqtSignal([bool], [int])
    exitClicked = pyqtSignal([bool], [int])

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__newGame, self.__controls, self.__highscores, self.__about, self.__exit = \
            [self.create_button(t) for t in ["New Game", "Control keys", "Highscores", "About", "Exit"]]
        self.__newGame.clicked.connect(self.newGameClicked)
        self.__controls.clicked.connect(self.controlsClicked)
        self.__highscores.clicked.connect(self.highscoresClicked)
        self.__about.clicked.connect(self.aboutClicked)
        self.__exit.clicked.connect(self.exitClicked)

        menu_label = QLabel("Cleaner Adventures")
        menu_label.setStyleSheet("font: bold; font-size: 72px; height: 120px; width: 120px;")
        menu_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        layout = QGridLayout()
        layout.addWidget(menu_label, 0, 0, 4, 5)
        layout.addWidget(self.__newGame, 4, 2, 2, 1)
        layout.addWidget(self.__controls, 6, 2, 2, 1)
        layout.addWidget(self.__highscores, 8, 2, 2, 1)
        layout.addWidget(self.__about, 10, 2, 2, 1)
        layout.addWidget(self.__exit, 12, 2, 2, 1)

        self.setLayout(layout)

    # slots
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.returnClicked.emit(Menu.RETURN)

    @staticmethod
    def create_button(text):
        button = QPushButton(text)
        button.setDefault(True)
        button.setStyleSheet("QPushButton { font: bold; border: 3px solid darkgrey; border-radius: 20px;"
                             "outline-radius: 20px; font-size: 32px; height: 60px; width: 120px; }"
                             "QPushButton:focus { font: bold; border: 10px solid white; border-radius: 20px;"
                             "outline-radius: 20px; font-size: 32px }")
        return button
