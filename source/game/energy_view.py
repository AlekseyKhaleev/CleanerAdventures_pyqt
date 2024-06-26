from dataclasses import dataclass

from PyQt6.QtCore import QRect, pyqtSlot
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtWidgets import QWidget, QSizePolicy


@dataclass(frozen=True)
class Energy:
    en_0: int = 0
    en_10: int = 1
    en_30: int = 2
    en_50: int = 3
    en_70: int = 4
    en_80: int = 5
    en_90: int = 6


class EnergyView(QWidget):
    __enStatusImgs = [QImage(f"resources/images/en_{perc}") for perc in (0, 10, 30, 50, 70, 80, 90)]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Ignored)
        self.__enStatus = Energy.en_90
        self.repaint()

    # slots
    @pyqtSlot()
    def paintEvent(self, event):
        self.__draw_status()

    @pyqtSlot()
    def __draw_status(self):
        qp = QPainter(self)
        qp.drawImage(QRect(int(self.width() / 2 - self.width() * 0.3), 0, int(self.width() * 0.6), self.height()),
                     self.__enStatusImgs[self.__enStatus])

    @pyqtSlot(int)
    def update_model(self, perc_energy):
        if perc_energy == 0:
            self.__enStatus = Energy.en_0
        elif perc_energy <= 10:
            self.__enStatus = Energy.en_10
        elif perc_energy <= 30:
            self.__enStatus = Energy.en_30
        elif perc_energy <= 50:
            self.__enStatus = Energy.en_50
        elif perc_energy <= 70:
            self.__enStatus = Energy.en_70
        elif perc_energy <= 80:
            self.__enStatus = Energy.en_80
        else:
            self.__enStatus = Energy.en_90
        self.repaint()
