from enum import Enum


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coordinates = (x, y)


class Colors(Enum):
    WHITE = (255, 255, 255)
    RED = (200, 0, 0)
    GREEN1 = (0, 210, 0)
    GREEN2 = (0, 150, 0)
    BLACK = (0, 0, 0)
