from PyQt6.QtCore import pyqtSlot, QObject, QCoreApplication
from PyQt6.QtWidgets import QWidget, QStackedLayout

from AboutWidget import AboutWidget
from AuthWidget import AuthWidget
from ControlsWidget import ControlsWidget
from GameWidget import GameWidget
from HighscoresWidget import HighscoresWidget
from MenuWidget import Menu, MenuWidget


class MainWidget(QWidget):
    # public
    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self.__menu = MenuWidget()
        self.__layout = QStackedLayout()
        self.__controls = ControlsWidget()
        self.__auth = AuthWidget()
        self.__about = AboutWidget()
        self.__highscores = HighscoresWidget()
        self.__game = None

        self.setStyleSheet("QWidget {background-color: black; color: WHITE;}")

        # -----------------------------------CONNECTIONS------------------------------------------------
        # SENDER: __menu
        self.__menu.newGameClicked.connect(self.change_widgets)
        self.__menu.controlsClicked.connect(self.change_widgets)
        self.__menu.highscoresClicked.connect(self.change_widgets)
        self.__menu.aboutClicked.connect(self.change_widgets)
        self.__menu.exitClicked.connect(self.change_widgets)
        self.__menu.returnClicked.connect(self.change_widgets)
        # SENDER: others
        self.__controls.returnClicked.connect(self.change_widgets)
        self.__about.returnClicked.connect(self.change_widgets)
        self.__highscores.returnClicked.connect(self.change_widgets)
        self.__auth.nameChanged.connect(self.init_new_game)

        # ---------------------------------END CONNECTIONS----------------------------------------------

        self.__layout.setStackingMode(QStackedLayout.StackingMode.StackOne)
        self.__layout.addWidget(self.__menu)
        self.__layout.addWidget(self.__controls)
        self.__layout.addWidget(self.__auth)
        self.__layout.addWidget(self.__about)
        self.__layout.addWidget(self.__highscores)

        self.setLayout(self.__layout)

    # public slots
    @pyqtSlot(int)
    def change_widgets(self, button: int):
        match button:
            case Menu.NEW_GAME:
                self.__layout.setCurrentWidget(self.__auth)
            case Menu.RETURN:
                if self.__layout.currentWidget() == self.__menu and self.__game is not None:
                    self.__layout.setCurrentWidget(self.__game)
                else:
                    self.__layout.setCurrentWidget(self.__menu)
            case Menu.CONTROLS:
                self.__layout.setCurrentWidget(self.__controls)
            case Menu.HIGHSCORES:
                self.__highscores.read_high_scores()
                self.__layout.setCurrentWidget(self.__highscores)
            case Menu.ABOUT:
                self.__layout.setCurrentWidget(self.__about)
            case Menu.EXIT:
                QCoreApplication.quit()
            case Menu.END_GAME:
                self.__layout.setCurrentWidget(self.__menu)
                self.__layout.removeWidget(self.__game)
                self.__game = None
            case _:
                pass

    @pyqtSlot(str)
    def init_new_game(self, name: str):
        if self.__game:
            self.__layout.removeWidget(self.__game)
        self.__game = GameWidget(name)

        # ----connections----
        self.__game.return_clicked.connect(self.change_widgets)
        self.__menu.exitClicked.connect(self.__game.write_highscore)
        # ---end connections-----
        self.__layout.addWidget(self.__game)
        self.__layout.setCurrentWidget(self.__game)
