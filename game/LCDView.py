from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QPushButton, QLCDNumber

import MazeModel, RobotModel

class LCDView(QLCDNumber):

    def __init__(self, model, parent=None):
        QLCDNumber.__init__(parent)
        self.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        if type(model) is MazeModel.model:
            self.setDigitCount(self.getRange(model.level))
            self.display(model.level)
        elif type(model) is RobotModel.model:
            self.setDigitCount(self.getRange(model.score))
            self.display(model.score)

    # slots
    def updateModel(self, model):
        if type(model) is MazeModel.model:
            self.setDigitCount(self.getRange(model.level))
            self.display(model.level)
        elif type(model) is RobotModel.model:
            self.setDigitCount(self.getRange(model.score))
            self.display(model.score)

    @staticmethod
    def getRange(value):
        rang = 0
        while not value:
            rang += 1
            value /= 10
        return [0, rang][bool(rang)]

