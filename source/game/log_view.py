import copy

from PyQt6.QtCore import Qt, QTime
from PyQt6.QtWidgets import QListWidget, QSizePolicy, QVBoxLayout

from source.mvc.robot_model import Model, States
from source.mvc.robot_view import RobotView


class LogView(RobotView):

    def __init__(self, target_model: Model, parent=None):
        super().__init__(copy.deepcopy(target_model), parent)
        self.__view_model = copy.deepcopy(target_model)
        self.__logs = QListWidget()
        self.__logs.setItemAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__logs.setStyleSheet("border: 6px solid white; font: bold; font-size: 14px")
        self.__logs.addItem(QTime.currentTime().toString() + "   -   " + States.descriptions[self.get_state()])
        self.__logs.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.__logs.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.__logs.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Ignored)
        layout = QVBoxLayout()
        layout.addWidget(self.__logs)
        self.setLayout(layout)

    def update_model(self, model: Model):
        if model.state != self.__view_model.state:
            self.__view_model = copy.deepcopy(model)
            if self.__view_model.state == States.INIT:
                self.__logs.clear()
            self.__logs.addItem(
                QTime.currentTime().toString() + "   -   " + States.descriptions[self.__view_model.state])
            self.__logs.scrollToBottom()

    def paintEvent(self, event):
        pass
