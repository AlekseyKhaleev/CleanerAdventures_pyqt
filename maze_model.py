import math
import random
from collections import deque
from dataclasses import dataclass, field

from PyQt6.QtCore import pyqtSignal, pyqtSlot, QPoint, QObject, QTime
from PyQt6.QtGui import QGuiApplication


@dataclass
class Model:
    DOT_SIDE: int = 32
    level: int = 0
    fieldWidth: int = 0
    fieldHeight: int = 0
    maxEnergy: int = 0
    walls: set[QPoint] = field(default_factory=lambda: {QPoint(0, 0)})
    cells: set[QPoint] = field(default_factory=lambda: {QPoint(1, 1)})
    batteries: deque[QPoint] = field(default_factory=lambda: deque((QPoint(-1, -1),)))
    targetPosition: QPoint = QPoint()


class MazeModel(QObject):
    # signals
    modelChanged = pyqtSignal(Model)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__model = Model()

        self.__init_field_size()
        self.init_maze()

    # public slots
    @pyqtSlot(QPoint)
    def add_battery(self, value: QPoint):
        self.__model.batteries.append(value)
        self.modelChanged.emit(self.__model)

    @pyqtSlot(QPoint)
    def del_battery(self, value: QPoint):
        while value in self.__model.batteries:
            self.__model.batteries.remove(value)
        self.modelChanged.emit(self.__model)

    @pyqtSlot()
    def step_back(self):
        self.__model.batteries.clear()
        self.modelChanged.emit(self.__model)

    @pyqtSlot()
    def init_maze(self):
        self.__init_default_maze_map()
        self.__locate_walls()
        if self.__model.batteries:
            self.__model.batteries.clear()
        self.__model.batteries.append(QPoint(-1, -1))
        # self.__model.targetPosition = QPoint(self.__model.fieldWidth - 2, self.__model.fieldHeight - 2)
        self.__model.targetPosition = sorted(self.__model.cells, key=lambda p: (p.x(), p.y()))[-1]
        self.__set_max_energy()
        self.__model.level += 1
        self.modelChanged.emit(self.__model)

    @pyqtSlot(bool)
    def reset_level(self, success: bool):
        if success:
            self.__model.level = 0

    @pyqtSlot()
    def get_model(self):
        return self.__model

    # private section
    def __init_field_size(self):
        rec = QGuiApplication.primaryScreen().size()
        self.__model.fieldWidth = math.floor(rec.width() / self.__model.DOT_SIDE)
        self.__model.fieldHeight = math.floor((rec.height() * 0.8) / self.__model.DOT_SIDE)

    def __init_default_maze_map(self):
        self.__model.cells.clear()
        self.__model.walls.clear()
        for y in range(self.__model.fieldHeight):
            for x in range(self.__model.fieldWidth):
                dot = QPoint(x, y)
                if (x % 2 and y % 2) and (y < self.__model.fieldHeight - 1 and x < self.__model.fieldWidth - 1):
                    self.__model.cells.add(dot)
                else:
                    self.__model.walls.add(dot)

    def __locate_walls(self):
        cells = set([k for k in self.__model.cells])
        current = self.__get_rand_dot()
        next_p, neighbours, way = QPoint(), deque(), deque()

        def do_while_body():
            nonlocal cells, current, neighbours, way, next_p
            neighbours = self.__get_maze_neighbours(current, cells)
            if neighbours:
                next_p = neighbours[random.randrange(len(neighbours))]
                way.append(QPoint(current))
                to_del = QPoint(current)
                if current.y() == next_p.y():
                    to_del.setX(current.x() + ((next_p.x() - current.x()) // (abs(next_p.x() - current.x()))))
                else:
                    to_del.setY(current.y() + ((next_p.y() - current.y()) // (abs(next_p.y() - current.y()))))
                if to_del in self.__model.walls:
                    self.__model.walls.remove(to_del)
                self.__model.cells.add(QPoint(to_del))
                current = next_p
                cells.remove(current)
            elif way:
                current = way.pop()
            else:
                current = list(cells)[random.randrange(len(cells))]

        do_while_body()
        while cells:
            do_while_body()

    def __get_rand_dot(self):
        time = QTime.currentTime()
        random.seed = time.msec()
        r_dot = lambda: QPoint(*(random.randrange(self.__model.fieldWidth), random.randrange(self.__model.fieldHeight)))
        dot = r_dot()
        while dot in self.__model.walls:
            dot = r_dot()
        return dot

    def __set_max_energy(self):
        self.__model.maxEnergy = 2
        cells = set(self.__model.cells)
        current, neighbours, way = QPoint(1, 1), deque(), deque()
        cells.remove(current)
        while current != self.__model.targetPosition:
            neighbours = self.__get_way_neighbours(current, cells)
            if neighbours:
                way.append(QPoint(current))
                current = neighbours[random.randrange(len(neighbours))]
                cells.remove(current)
            elif way:
                current = way.pop()
            else:
                break
        self.__model.maxEnergy += len(way)
        for i in range(1, len(way)-1):
            if (way[i - 1].x() == way[i].x() and way[i + 1].y() == way[i].y()) or (
                    way[i - 1].y() == way[i].y() and way[i + 1].x() == way[i].x()):
                self.__model.maxEnergy += 1

    @staticmethod
    def __get_maze_neighbours(current: QPoint, cells: set[QPoint]) -> deque[QPoint]:
        cur_neighbours = deque()
        tmp = QPoint(current)

        def check_next(nx: int, ny: int):
            nonlocal tmp
            tmp.setX(tmp.x() + nx)
            tmp.setY(tmp.y() + ny)
            if tmp in cells:
                return QPoint(tmp)

        for x, y in zip((2, -4, 2, 0), (0, 0, 2, -4)):
            if neighbour := check_next(x, y):
                cur_neighbours.append(neighbour)
        return cur_neighbours

    @staticmethod
    def __get_way_neighbours(current: QPoint, cells: set[QPoint]) -> deque[QPoint]:
        cur_neighbours = deque()
        tmp = QPoint(current)

        def check_next(nx: int, ny: int):
            nonlocal tmp
            tmp.setX(tmp.x() + nx)
            tmp.setY(tmp.y() + ny)
            if tmp in cells:
                return QPoint(tmp)

        for x, y in zip((1, -2, 1, 0), (0, 0, 1, -2)):
            if neighbour := check_next(x, y):
                cur_neighbours.append(neighbour)
        return cur_neighbours
