from dataclasses import dataclass


@dataclass
class GameData:
    DOT_SIZE: int = 64

    @staticmethod
    def decrease_dot_size(level: int):
        if level == 1:
            GameData.DOT_SIZE = 64
        elif GameData.DOT_SIZE <= 10:
            GameData.DOT_SIZE = 10
        else:
            GameData.DOT_SIZE = GameData.DOT_SIZE - 2
