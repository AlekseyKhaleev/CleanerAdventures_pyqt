from copy import deepcopy

from PyQt6.QtCore import pyqtSignal, pyqtSlot, QPoint, QObject, Qt, QTimer, QTime

import random
import HighscoresWidget
import MazeModel
import MenuWidget
import RobotModel


class Controller(QObject):
    # signals
    batteryFound = pyqtSignal(QPoint)
    batteryLocated = pyqtSignal(QPoint)
    energyChanged = pyqtSignal(int)
    levelDone = pyqtSignal(bool)
    reset_maze = pyqtSignal()
    reset_robot = pyqtSignal()
    return_clicked = pyqtSignal(int)
    robot_moved = pyqtSignal(QPoint, int, int)
    robot_rotated = pyqtSignal(int, int)
    skin_animated = pyqtSignal()
    step_back = pyqtSignal()

    # public slots
    @pyqtSlot
    def exit(self):
        self.write_highscore()
        self.return_clicked.emit(MenuWidget.Menu.END_GAME)

    @pyqtSlot(int)
    def key_event_action(self, key: int):
        match key:
            case Qt.Key.Key_Left:
                if self.__robot_model.robotDestination != RobotModel.Directions.LEFT:
                    self.robot_rotated.emit(RobotModel.Directions.LEFT, self.__check_energy())
            case Qt.Key.Key_Right:
                if self.__robot_model.robotDestination != RobotModel.Directions.LEFT:
                    self.robot_rotated.emit(RobotModel.Directions.LEFT, self.__check_energy())
            case Qt.Key.Key_Up:
                if self.__robot_model.robotDestination != RobotModel.Directions.UP:
                    self.robot_rotated.emit(RobotModel.Directions.UP, self.__check_energy())
            case Qt.Key.Key_Down:
                if self.__robot_model.robotDestination != RobotModel.Directions.DOWN:
                    self.robot_rotated.emit(RobotModel.Directions.DOWN, self.__check_energy())
            case Qt.Key.Key_Space:
                self.__move_robot()
            case Qt.Key.Key_Escape:
                self.return_clicked.emit(MenuWidget.Menu.RETURN)
            case _:
                pass
        if self.__robot_model.steps == self.__maze_model.maxEnergy:
            self.levelDone.emit(False)

    @pyqtSlot(MazeModel.Model)
    def update_maze_model(self, model: MazeModel.Model):
        self.__maze_model = deepcopy(model)

    @pyqtSlot(RobotModel.Model)
    def update_robot_model(self, model: RobotModel.Model):
        self.__robot_model = deepcopy(model)
        if self.__robot_model.state == RobotModel.States.INIT:
            self.__animation_timer.start(300)
        elif self.__robot_model.state == RobotModel.States.EXIT:
            self.__animation_timer.stop()
        if en := self.__get_percent_energy() or self.__robot_model.steps >= self.__maze_model.maxEnergy:
            self.energyChanged.emit(en)

    @pyqtSlot
    def write_highscore(self):
        with open("../resources/highscores.txt", "r") as HSFile:
            data = [line.replace("\n", "") for line in HSFile.readlines()]
            old_lines = [HighscoresWidget.Line(n, s) for n, s in zip(data[::2], map(int, data[1::2]))]
            old_lines.append(HighscoresWidget.Line(self.__robot_model.name, self.__robot_model.score))
            old_lines.sort(key=lambda l: -l.SCORE)
        with open("../resources/highscores.txt", "w") as HSFile:
            HSFile.writelines([line.NAME + "\n" + str(line.SCORE) + "\n" for line in old_lines[:9]])

    # public
    def __init__(self, robot_model: RobotModel.Model, maze_model: MazeModel.Model, parent=None):
        QObject.__init__(self, parent)
        self.__robot_model = deepcopy(robot_model)
        self.__maze_model = deepcopy(maze_model)
        self.__score_increase = True
        self.__animation_timer = QTimer()
        self.__animation_timer.start(300)
        self.__animation_timer.timeout.connect(self.skin_animated)

    # private
    def __check_wall(self, dest):
        return dest not in self.__maze_model.walls

    def __get_percent_energy(self):
        return ((self.__maze_model.maxEnergy - self.__robot_model.steps) * 100) // self.__maze_model.maxEnergy

    def __update_score(self):
        if self.scoreIncrease:
            return self.__robot_model.score + 1
        elif self.__robot_model.score:
            return self.__robot_model.score - 1
        else:
            return self.__robot_model.score

    def __check_battery(self):
        if self.__robot_model.robotPosition in self.__maze_model.batteries:
            self.scoreIncrease = False
            self.batteryFound.emit(self.__robot_model.robotPosition)
            self.energyChanged.emit(self.__get_percent_energy())

    def __check_target(self):
        if self.__robot_model.robotPosition == self.__maze_model.targetPosition:
            self.scoreIncrease = True
            self.levelDone.emit(True)

    def __locate_battery(self):
        battery = self.__get_rand_dot()
        while (self.__robot_model.robotPosition == battery) or (self.__maze_model.targetPosition == battery) or (
                abs(battery.x() - self.__robot_model.robotPosition.x()) > self.__maze_model.fieldWidth / 4) or (
                abs(battery.y() - self.__robot_model.robotPosition.y()) > self.__maze_model.fieldHeight / 2):
            battery = self.__get_rand_dot()
        self.batteryLocated.emit(battery)

    def __move_robot(self):
        tar_pos = deepcopy(self.__robot_model.robotPosition)
        match self.__robot_model.robotDestination:
            case RobotModel.Directions.LEFT:
                tar_pos.setX(tar_pos.x() - 1)
                if self.__check_wall(tar_pos):
                    self.robot_moved.emit(tar_pos, self.__update_score(), self.__check_energy())
            case RobotModel.Directions.RIGHT:
                tar_pos.setX(tar_pos.x() + 1)
                if self.__check_wall(tar_pos):
                    self.robot_moved.emit(tar_pos, self.__update_score(), self.__check_energy())
            case RobotModel.Directions.UP:
                tar_pos.setX(tar_pos.y() - 1)
                if self.__check_wall(tar_pos):
                    self.robot_moved.emit(tar_pos, self.__update_score(), self.__check_energy())
            case RobotModel.Directions.DOWN:
                tar_pos.setX(tar_pos.y() + 1)
                if self.__check_wall(tar_pos):
                    self.robot_moved.emit(tar_pos, self.__update_score(), self.__check_energy())
            case _:
                pass

        self.__check_target()
        self.__check_battery()

    def __get_rand_dot(self):
        time = QTime.currentTime()
        random.seed = time.msec()
        r_dot = lambda: QPoint(*(random.randrange(self.__maze_model.fieldWidth),
                                 random.randrange(self.__maze_model.fieldHeight)))
        dot = r_dot()
        while dot in self.__maze_model.walls:
            dot = r_dot()
        return dot

    def __check_energy(self):
        cur_energy = self.__get_percent_energy()
        if self.__robot_model.steps == self.__maze_model.maxEnergy:
            return RobotModel.Colors.WHITE

        if ((cur_energy <= 70) and ((self.__robot_model.curColor == RobotModel.Colors.GREEN) or (
                self.__robot_model.tmpColor == RobotModel.Colors.GREEN))):
            self.__locate_battery()
            return RobotModel.Colors.YELLOW
        if ((cur_energy <= 30) and ((self.__robot_model.curColor == RobotModel.Colors.YELLOW) or (
                self.__robot_model.tmpColor == RobotModel.Colors.YELLOW))):
            self.__locate_battery()
            return RobotModel.Colors.RED
        return [self.__robot_model.tmpColor, self.__robot_model.curColor][
            self.__robot_model.tmpColor == RobotModel.Colors.WHITE]
