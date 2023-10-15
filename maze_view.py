from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QImage, QPainter, QColor
from PyQt6.QtWidgets import QWidget, QStyleOption, QStyle

from maze_model import Model as MModel


class MazeView(QWidget):
    def __init__(self, target_model: MModel, parent=None):
        QWidget.__init__(self, parent)
        self.__view_model = target_model
        self.__battery_image = QImage(":/images/battery.png")
        self.__target_image = QImage(":/images/target.png")
        self.repaint()

    def draw_maze(self):
        qp = QPainter(self)
        dot_side = MModel.DOT_SIDE
        for w in self.__view_model.walls:
            qp.setBrush(QColor(Qt.GlobalColor.black))
            qp.drawRect(w.x() * dot_side, w.y() * dot_side, dot_side, dot_side)

    def draw_target(self):
        qp = QPainter(self)
        dot_side = MModel.DOT_SIDE
        qp.drawImage(QRect(self.__view_model.targetPosition.x() * dot_side,
                           self.__view_model.targetPosition.y() * dot_side, dot_side, dot_side), self.__target_image)

    def draw_battery(self):
        qp = QPainter(self)
        dot_side = MModel.DOT_SIDE
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
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, qp, self)

        self.draw_maze()
        self.draw_target()
        self.draw_battery()
