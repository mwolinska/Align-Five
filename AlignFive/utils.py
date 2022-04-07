from dataclasses import dataclass
from typing import List, Tuple

import numpy as np


def find_index_of_closest_value(click: int, allowed_positions_list: List[int]) -> int:
    allowed_positions_array = np.asarray(allowed_positions_list)
    closest_position_index = (np.abs(allowed_positions_array - click)).argmin()
    return closest_position_index

@dataclass
class Click(object):
    x: int
    y: int

@dataclass
class Position(object):
    row: int
    column: int

    @classmethod
    def from_tuple(cls, position):
        return cls(position[0], position[1])

    @classmethod
    def from_index(cls, index, n_columns:int):
        return cls((index // n_columns), (index % n_columns))

@dataclass
class PositionIndex(object):
    position_index: int

    @classmethod
    def from_position(cls, position: Position, n_columns: int):
        return position.row * n_columns + position.column

@dataclass
class Move(object):
    position: Position
    player_number: int

@dataclass
class Color(object):
    r: int
    g: int
    b: int

    @property
    def rgb(self) -> Tuple[int, int, int]:
        return self.r, self.g, self.b



