from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QPushButton


class GameOverView(QMessageBox):
    # signals
    gameStarted = pyqtSignal()
    gameEnded = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__accept = self.createButton("")
        self.__exit = self.createButton("I'LL BE BACK")
        self.setStyleSheet(
            "QMessageBox { font: bold; font-size: 36px; border: 6px solid grey; background-color: black; } "
            "QLabel { color: white; min-width: 240px; min-height: 120px }"
            "QPushButton { color: white; min-width: 240px }")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowSystemMenuHint)
        self.setDefaultButton(self.__accept)

    # slots
    def levelDone(self, success):
        if success:
            self.__accept.setText("GO NEXT!")
            self.setText("<p align='center'>Level done, great! </p>")
            self.setInformativeText("<p align=center>Go next?</p>")
        else:
            self.__accept.setText("TRY AGAIN!")
            self.setText("<p align='center'>Ohh no! You lose!</p>")
            self.setInformativeText("<p align=center>Wanna try again?</p>")
        self.addButton(self.__exit, QMessageBox.ButtonRole.RejectRole)
        self.addButton(self.__accept, QMessageBox.ButtonRole.AcceptRole)
        self.__accept.setDefault(True)

        self.exec()
        if self.clickedButton() != self.__accept:
            self.gameEnded.emit()
        else:
            self.gameStarted.emit()

    @staticmethod
    def createButton(text):
        button = QPushButton(text)
        button.setStyleSheet("QPushButton { font: bold; border: 3px solid darkgrey; border-radius: 20px;"
                             "outline-radius: 20px; font-size: 18px; height: 60px; width: 120px; }"
                             "QPushButton:focus { font: bold; border: 10px solid white; border-radius: 20px;"
                             "outline-radius: 20px; font-size: 18px }")
        return button

