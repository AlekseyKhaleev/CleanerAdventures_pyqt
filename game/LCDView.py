from PyQt6.QtWidgets import QLCDNumber

import MazeModel
import RobotModel


class LCDView(QLCDNumber):

    def __init__(self, model, parent=None):
        QLCDNumber.__init__(parent)
        self.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        if type(model) is MazeModel.Model:
            self.setDigitCount(self.get_range(model.level))
            self.display(model.level)
        elif type(model) is RobotModel.Model:
            self.setDigitCount(self.get_range(model.score))
            self.display(model.score)

    # slots
    def update_model(self, model):
        if type(model) is MazeModel.Model:
            self.setDigitCount(self.get_range(model.level))
            self.display(model.level)
        elif type(model) is RobotModel.Model:
            self.setDigitCount(self.get_range(model.score))
            self.display(model.score)

    @staticmethod
    def get_range(value):
        rang = 0
        while not value:
            rang += 1
            value /= 10
        return [0, rang][bool(rang)]
