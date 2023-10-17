from dataclasses import dataclass


@dataclass
class GameData:
    DOT_SIZE: int = 64

    @staticmethod
    def set_dot_size(level: int):
        if level == 1:
            GameData.DOT_SIZE = 64
        elif GameData.DOT_SIZE - level <= 0:
            GameData.DOT_SIZE = 1
        else:
            GameData.DOT_SIZE = GameData.DOT_SIZE - level

