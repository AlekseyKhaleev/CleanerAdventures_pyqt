from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QImage, QPainter, QColor, QPixmap
from PyQt6.QtWidgets import QWidget, QStyleOption, QStyle

from maze_model import Model as MModel
from game_data import GameData


class MazeView(QWidget):
    def __init__(self, target_model: MModel, parent=None):
        super().__init__(parent)
        self.__view_model = target_model
        self.__battery_image = QImage("resources/images/battery.png")
        self.__target_image = QImage("resources/images/target.png")
        self.repaint()

    def draw_maze(self, qp: QPainter):
        dot_side = GameData.DOT_SIZE
        for c in self.__view_model.cells:
            qp.setBrush(QColor(Qt.GlobalColor.white))
            qp.drawRect(c.x() * dot_side, c.y() * dot_side, dot_side, dot_side)

    def draw_target(self, qp: QPainter):
        dot_side = GameData.DOT_SIZE

        qp.drawImage(QRect(self.__view_model.targetPosition.x() * dot_side,
                           self.__view_model.targetPosition.y() * dot_side, dot_side, dot_side), self.__target_image)

    def draw_battery(self, qp: QPainter):
        dot_side = GameData.DOT_SIZE
        for b in self.__view_model.batteries:
            if b.x() >= 0:
                qp.drawImage(QRect(b.x() * dot_side, b.y() * dot_side, dot_side, dot_side), self.__battery_image)

    def update_model(self, model: MModel):
        self.__view_model = model
        self.repaint()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        qp = QPainter(self)
        qp.begin(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, qp, self)

        self.draw_maze(qp)
        self.draw_target(qp)
        self.draw_battery(qp)
        qp.end()