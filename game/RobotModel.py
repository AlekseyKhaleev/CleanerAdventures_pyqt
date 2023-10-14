from dataclasses import dataclass
from PyQt6.QtCore import pyqtSignal, QPoint, QObject
from collections import deque


@dataclass(frozen=True)
class Directions:
    LEFT: int = 0
    RIGHT: int = 1
    UP: int = 2
    DOWN: int = 3


@dataclass(frozen=True)
class Colors:
    WHITE: int = 0
    GREEN: int = 1
    YELLOW: int = 2
    RED: int = 3


@dataclass(frozen=True)
class States:
    WAIT: int = 0
    MOVE: int = 1
    REPLACE_BATTERY: int = 2
    ROTATE: int = 3
    STEP_BACK: int = 4
    EXIT: int = 5


@dataclass
class Model:
    curColor: int = 0
    tmpColor: int = 0
    robotDestination: int = 0

    DOT_SIDE: int = 34
    score: int = 0
    highScore: int = 0
    steps: int = 0
    name: str = ""
    state: int = 0
    robotPosition: QPoint = QPoint()


class RobotModel(QObject):

    # signals
    modelChanged = pyqtSignal(Model)

    def __init__(self, name, parent=None):
        QObject.__init__(self, parent)
        self.__model = Model()
        self.__memory = deque()
        self.__model.name = name
        self.init_robot()

    # public slots
    def init_robot(self):
        self.__model.state = States.WAIT
        self.__model.robotDestination = Directions.UP
        self.__model.robotPosition = QPoint(1, 1)
        self.__model.curColor = Colors.GREEN
        self.__model.tmpColor = Colors.WHITE
        self.__model.steps = 0
        self.__memory.clear()
        self.__memory.append(self.__model)
        if self.__model.score:
            self.__model.score += 100
        self.modelChanged(self.__model).emit()

    def step_back(self):
        if self.__memory:
            last_model = self.__memory.pop()
            if last_model.steps == self.__model.steps:
                self.step_back()
            else:
                self.__model.robotPosition = last_model.robotPosition
                self.__model.robotDestination = last_model.robotDestination
                self.__model.score = last_model.score
                self.__model.steps = last_model.steps
                self.__model.curColor = last_model.curColor
                self.__model.tmpColor = last_model.tmpColor
                self.__model.state = States.STEP_BACK
                self.modelChanged(self.__model).emit()

            if not self.__memory:
                self.__memory.append(self.__model)

    def move(self, tar_pos, score, color):
        self.__model.state = States.MOVE
        self.__model.steps += 1
        self.__model.robotPosition = tar_pos
        self.__model.score = score
        self.__model.curColor = color
        self.__model.tmpColor = Colors.WHITE
        self.__memory.append(self.__model)
        self.modelChanged(self.__model).emit()

    def wait(self):
        self.__model.state = States.WAIT
        self.__model.curColor, self.__model.tmpColor = self.__model.tmpColor, self.__model.curColor
        self.modelChanged(self.__model).emit()

    def get_model(self):
        return self.__model

    def replace_battery(self, bat_pos=None):
        self.__model.state = States.REPLACE_BATTERY
        self.__model.steps = 0
        self.__model.score += 50
        self.__model.curColor = Colors.GREEN
        self.__model.tmpColor = Colors.WHITE
        self.__memory.append(self.__model)
        self.modelChanged(self.__model).emit()

    def exit(self, success):
        self.__model.state = States.EXIT
        if not success:
            self.__model.score = 0
            self.__model.highScore = 0
            self.__model.curColor = Colors.WHITE
            self.__model.tmpColor = Colors.WHITE
        else:
            self.__model.highScore += self.__model.score
        self.modelChanged(self.__model).emit()
