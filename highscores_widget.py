from dataclasses import dataclass

from PyQt6.QtCore import pyqtSignal, Qt, QFile, QIODevice
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy

from menu_widget import Menu


@dataclass
class Line:
    NAME: str
    SCORE: int

    def __gt__(self, other):
        return self.SCORE > other.SCORE

    def __lt__(self, other):
        return self.SCORE < other.SCORE

    def __ge__(self, other):
        return self.SCORE >= other.SCORE

    def __le__(self, other):
        return self.SCORE <= other.SCORE

    def __eq__(self, other):
        return self.SCORE == other.SCORE


class HighscoresWidget(QWidget):
    # signals
    returnClicked = pyqtSignal(int)
    __FileLines, __LayLines = None, None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__LayLines = [] if self.__LayLines is None else ...
        self.__FileLines = [] if self.__FileLines is None else ...
        self.__HS_file_path = "resources/highscores.txt"
        self.__layout = QGridLayout()
        self.setLayout(self.__layout)

    # slots
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.returnClicked.emit(Menu.RETURN)

    def read_high_scores(self):
        self.__FileLines.clear()
        with open(self.__HS_file_path, "r") as hs_file:
            data = [line.replace("\n", "") for line in hs_file.readlines()]
            self.__FileLines = [Line(n, s) for n, s in zip(data[::2], map(int, data[1::2]))]
            self.__create_lay_lines()

    def __create_lay_lines(self):
        while self.__layout.takeAt(0) is not None:
            self.__layout.removeItem(self.__layout.takeAt(0))
        title = QLabel("Highscores: ")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("QLabel { font: bold; font-size: 72px }")
        self.__layout.addWidget(title, 0, 0, 2, 5)
        for i in range(10):
            if i >= len(self.__FileLines):
                break
            self.__layout.addWidget(self.create_label(str(i + 1) + '. '), 2 + i, 1, 1, 1, Qt.AlignmentFlag.AlignRight)
            self.__layout.addWidget(self.create_label(self.__FileLines[i].NAME), 2 + i, 2, 1, 1)
            self.__layout.addWidget(self.create_label(str(self.__FileLines[i].SCORE)), 2 + i, 3, 1, 1)

    @staticmethod
    def create_label(text):
        label = QLabel(text)
        label.setStyleSheet("QLabel { font: bold; font-size: 32px }")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        return label
