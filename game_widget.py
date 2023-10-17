from PyQt6.QtCore import pyqtSignal, QObject, Qt
from PyQt6.QtWidgets import QWidget, QLabel, QStackedLayout, QGridLayout

from controller import Controller
from energy_view import EnergyView
from game_over_view import GameOverView
from lcd_view import LCDView
from log_view import LogView
from maze_model import MazeModel
from maze_view import MazeView
from robot_model import RobotModel
from robot_view import RobotView


class GameWidget(QWidget):
    # signals
    write_highscore = pyqtSignal()
    return_clicked = pyqtSignal(int)

    # public
    def __init__(self, name: str, parent: QObject | None = None):
        super().__init__(parent)
        self.__robot_model = RobotModel(name)
        self.__maze_model = MazeModel()
        self.__energyView = EnergyView()
        self.__gameOverView = GameOverView()
        self.__controller = Controller(self.__robot_model.get_model(), self.__maze_model.get_model())
        self.__robotView = RobotView(self.__robot_model.get_model())
        self.__mazeView = MazeView(self.__maze_model.get_model())
        self.__levelView = LCDView(self.__maze_model.get_model())
        self.__scoreView = LCDView(self.__robot_model.get_model())
        self.__logView = LogView(self.__robot_model.get_model())

        self.setStyleSheet("QWidget {background-color: black; color: WHITE;}")
        self.__robotView.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.__mazeView.setStyleSheet("MazeView {background-color: black; color: white;}")

        # -----------------------------------CONNECTIONS------------------------------------------------
        # SENDER: __gameOverView
        self.__gameOverView.gameStarted.connect(self.__controller.reset_maze)
        self.__gameOverView.gameStarted.connect(self.__controller.reset_robot)
        self.__gameOverView.gameEnded.connect(self.__controller.exit)
        # SENDER: __maze_model
        self.__maze_model.modelChanged.connect(self.__controller.update_maze_model)
        self.__maze_model.modelChanged.connect(self.__mazeView.update_model)
        self.__maze_model.modelChanged.connect(self.__levelView.update_model)
        # SENDER: __robot_model
        self.__robot_model.modelChanged.connect(self.__controller.update_robot_model)
        self.__robot_model.modelChanged.connect(self.__robotView.update_model)
        self.__robot_model.modelChanged.connect(self.__scoreView.update_model)
        self.__robot_model.modelChanged.connect(self.__logView.update_model)
        # SENDER: __robotView
        self.__robotView.key_handled.connect(self.__controller.key_event_action)
        # SENDER: __controller
        self.__controller.levelDone.connect(self.__robot_model.exit)
        self.__controller.levelDone.connect(self.__maze_model.reset_level)
        self.__controller.levelDone.connect(self.__gameOverView.levelDone)

        self.__controller.reset_maze.connect(self.__maze_model.init_maze)
        self.__controller.reset_robot.connect(self.__robot_model.init_robot)

        self.__controller.batteryFound.connect(self.__maze_model.del_battery)
        self.__controller.batteryFound.connect(self.__robot_model.replace_battery)
        self.__controller.batteryLocated.connect(self.__maze_model.add_battery)
        self.__controller.step_back.connect(self.__maze_model.step_back)
        self.__controller.step_back.connect(self.__robot_model.step_back)

        self.__controller.energyChanged.connect(self.__energyView.update_model)
        self.__controller.skin_animated.connect(self.__robot_model.wait)
        self.__controller.robot_rotated.connect(self.__robot_model.rotate)
        self.__controller.robot_moved.connect(self.__robot_model.move)
        self.__controller.return_clicked.connect(self.return_clicked)

        # SENDER: self
        self.write_highscore.connect(self.__controller.write_highscore)

        # ---------------------------------END CONNECTIONS----------------------------------------------

        game_lay = QStackedLayout()
        game_lay.setStackingMode(QStackedLayout.StackingMode.StackAll)
        game_lay.addWidget(self.__mazeView)
        game_lay.addWidget(self.__robotView)

        layout = QGridLayout()
        layout.addWidget(self.__create_label(self.__robot_model.get_model().name + " ENERGY"), 0, 0, 2, 1)
        layout.addWidget(self.__energyView, 2, 0, 3, 1)
        layout.addWidget(self.__create_label("STATE LOG"), 0, 1, 2, 1)
        layout.addWidget(self.__logView, 2, 1, 3, 1, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.__create_label("LEVEL"), 0, 2, 2, 1)
        layout.addWidget(self.__levelView, 2, 2, 3, 1)
        layout.addWidget(self.__create_label("SCORE"), 0, 3, 2, 1)
        layout.addWidget(self.__scoreView, 2, 3, 3, 1)
        layout.addLayout(game_lay, 6, 0, 20, 4)

        self.setLayout(layout)

    # private
    @staticmethod
    def __create_label(text: str):
        label = QLabel(text)
        label.setStyleSheet("QLabel { font: bold; font-size: 30px; }")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        return label
