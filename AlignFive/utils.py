from dataclasses import dataclass
from typing import List, Tuple, TYPE_CHECKING

import numpy as np


def find_index_of_closest_value(click: int, allowed_positions_list: List[int]) -> int:
    allowed_positions_array = np.asarray(allowed_positions_list)
    closest_position_index = (np.abs(allowed_positions_array - click)).argmin()
    return closest_position_index

@dataclass
class Position(object):
    x: int
    y: int

@dataclass
class Color(object):
    r: int
    g: int
    b: int

    @property
    def rgb(self) -> Tuple[int, int, int]:
        return self.r, self.g, self.b

