from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from MenuWidget import Menu


class AuthWidget(QWidget):
    # signals
    returnClicked = pyqtSignal(int)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        layout, title = QGridLayout(), QLabel("Control keys:")
        title.setStyleSheet("QLabel { font: bold solid black; font-size: 72px; }")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        [layout.addWidget(self.create_label(t), *pos) for t, pos in zip([
            [title, "Rotate robot: ", "Arrows", "Move robot: ", "Space", "Step Undo: ", "Backspace", "Menu / Return :",
             "ESC"],
            [(0, 0, 1, 6)] + [(x, y, 1, 1) for x in (1, 2, 3, 4) for y in (2, 3)]])]
        self.setLayout(layout)

    @staticmethod
    def create_label(text):
        label = QLabel(text)
        label.setStyleSheet("QLabel { font: bold; font-size: 36px; }")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.returnClicked.emit(Menu.RETURN)
