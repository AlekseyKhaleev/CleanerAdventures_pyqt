import copy

from PyQt6.QtCore import QRect, pyqtSignal
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtWidgets import QWidget, QSizePolicy
from dataclasses import dataclass
import RobotModel


class RobotView(QWidget):

    # signals
    key_handled = pyqtSignal(int)

    def __init__(self, target_model: RobotModel.Model, parent=None):
        QWidget.__init__(self, parent)
        self.__view_model = target_model

