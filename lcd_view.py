from PyQt6.QtWidgets import QLCDNumber

from maze_model import Model as MModel
from robot_model import Model as RModel


class LCDView(QLCDNumber):

    def __init__(self, model, parent=None):
        QLCDNumber.__init__(parent)
        self.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        if type(model) is MModel:
            self.setDigitCount(self.get_range(model.level))
            self.display(model.level)
        elif type(model) is RModel:
            self.setDigitCount(self.get_range(model.score))
            self.display(model.score)

    # slots
    def update_model(self, model):
        if type(model) is MModel:
            self.setDigitCount(self.get_range(model.level))
            self.display(model.level)
        elif type(model) is RModel:
            self.setDigitCount(self.get_range(model.score))
            self.display(model.score)

    @staticmethod
    def get_range(value):
        rang = 0
        while not value:
            rang += 1
            value /= 10
        return [0, rang][bool(rang)]
