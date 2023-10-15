import copy

from PyQt6.QtCore import QRect, pyqtSignal
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtWidgets import QWidget, QSizePolicy

import RobotModel


class RobotView(QWidget):
    # signals
    key_handled = pyqtSignal(int)

    def __init__(self, target_model: RobotModel.Model, parent=None):
        QWidget.__init__(self, parent)
        self.__view_model = target_model
        self.__white, self.__green, self.__yellow, self.__red = [
            [QImage(f":/images/VC_{col}_{dest}") for dest in ["lt", "rt", "up", "dn"]] for col in
            ["wt", "gr", "yw", "rd"]]
        self.__robot_skin = (self.__white, self.__green, self.__yellow, self.__red)

    def paintEvent(self, event):
        self.draw_robot()

    def keyPressEvent(self, event):
        self.key_handled.emit(event.key())

    def draw_robot(self):
        qp = QPainter(self)
        qp.drawImage(QRect(self.__view_model.robotPosition.x() * RobotModel.Model.DOT_SIDE,
                           self.__view_model.robotPosition.y() * RobotModel.Model.DOT_SIDE,
                           RobotModel.Model.DOT_SIDE, RobotModel.Model.DOT_SIDE),
                     self.__robot_skin[self.__view_model.curColor][self.__view_model.robotDestination])

    def update_model(self, model: RobotModel.Model):
        self.__view_model = model
        self.repaint()
