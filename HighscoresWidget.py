from dataclasses import dataclass

from PyQt6.QtCore import pyqtSignal, Qt, QFile, QIODevice
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy

from MenuWidget import Menu


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
    returnClicked = pyqtSignal(button=Menu.RETURN)
    __layout, __HSFile, __FileLines, __LayLines = None, None, None, None

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.__LayLines = [] if self.__LayLines is None else ...
        self.__FileLines = [] if self.__FileLines is None else ...
        __HSFile = QFile("../resources/highscores.txt")
        __layout = QGridLayout()
        self.setLayout(__layout)

    # slots
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.returnClicked().emit()

    def read_high_scores(self):
        self.__FileLines.clear()
        if self.__HSFile.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            while not self.__HSFile.atEnd():
                line_name = self.__HSFile.readline()
                line_name.remove("\n")
                line_score = self.__HSFile.readline()
                line_score.remove("\n")
                self.__FileLines.append(Line(line_name, int(line_score)))
            self.__HSFile.close()
            self.__create_lay_lines()

    def __create_lay_lines(self):
        while item := self.__layout.takeAt(0) is not None:
            del item.widget
            del item
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
