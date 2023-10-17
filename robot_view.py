from PyQt6.QtCore import QRect, pyqtSignal
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtWidgets import QWidget

from robot_model import Model as RModel
from game_data import GameData


class RobotView(QWidget):
    # signals
    key_handled = pyqtSignal(int)

    def __init__(self, target_model: RModel, parent=None):
        super().__init__(parent)
        self.__view_model = target_model
        self.__white, self.__green, self.__yellow, self.__red = [
            [QImage(f"resources/images/VC_{col}_{dest}.png") for dest in ["lt", "rt", "up", "dn"]] for col in
            ["wt", "gr", "yw", "rd"]]
        self.__robot_skin = (self.__white, self.__green, self.__yellow, self.__red)

    def paintEvent(self, event):
        self.draw_robot()

    def keyPressEvent(self, event):
        self.key_handled.emit(event.key())

    def draw_robot(self):
        dot_size = GameData.DOT_SIZE
        qp = QPainter(self)
        qp.drawImage(QRect(self.__view_model.robotPosition.x() * dot_size,
                           self.__view_model.robotPosition.y() * dot_size,
                           dot_size, dot_size),
                     self.__robot_skin[self.__view_model.curColor][self.__view_model.robotDestination])

    def update_model(self, model: RModel):
        self.__view_model = model
        self.repaint()

    def get_state(self):
        return self.__view_model.state
