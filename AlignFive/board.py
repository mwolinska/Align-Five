import logging
import random
import typing
from typing import List

import numpy as np

from AlignFive.game_interface import GameWindow
from AlignFive.utils import Position, Move

if typing.TYPE_CHECKING:
    pass


class GameBoard(object):
    def __init__(self, board_size: int = 19, generate_visual: bool = False):
        self.board = np.zeros((board_size, board_size))
        if generate_visual:
            self.game_visual = GameWindow()
        else:
            self.game_visual = None

        self.available_positions_list = self.get_array_of_indices()

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, array_board: np.ndarray):
        self._board = array_board

    @classmethod
    def from_array(cls, mid_game_board: np.ndarray, generate_visual: bool = False):
        game_board = cls(generate_visual=generate_visual)
        game_board.board = mid_game_board
        return game_board

    def get_array_of_indices(self):
        list_of_indices = []
        for i in range(self.board.size):
            list_of_indices.append(i)

        return np.array(list_of_indices)

    def list_available_position_indexes(self) -> List[int]:
        current_board = self.board.flatten()
        board_mask = current_board == 0
        list_of_board_indices = self.get_array_of_indices()
        return list_of_board_indices[board_mask]

    def is_position_available(self, selected_position: Position) -> bool:
        position_index = selected_position.row * self.board.shape[1] + selected_position.column
        if position_index in self.available_positions_list:
            return True
        else:
            return False

    def update_board(self, move: Move):
        self.board[move.position.row][move.position.column] = move.player_number
        self.available_positions_list = self.available_positions_list[self.available_positions_list != move.position.row * self.board.shape[1] + move.position.column]

    def count_neighbours(self, check_direction: Position, last_move: Move):

        is_neighbour_same_colour = True
        n_neighbouring_player_stones = 0
        next_field_increment = 1

        while is_neighbour_same_colour:
            next_row = last_move.position.row + (next_field_increment * check_direction.row)
            next_column = last_move.position.column + (next_field_increment * check_direction.column)

            if (next_row >= self.board.shape[0] or next_row < 0) or (next_column >= self.board.shape[1] or next_column < 0):
                return n_neighbouring_player_stones
            logging.debug(f"{next_row}, {next_column}")
            neighbour_value = self.board[next_row][next_column]

            if neighbour_value == last_move.player_number:
                n_neighbouring_player_stones += 1
                next_field_increment += 1
            else:
                is_neighbour_same_colour = False

        return n_neighbouring_player_stones



if __name__ == '__main__':
    board = GameBoard(board_size=3).from_array(np.array(
    [
        [1, 1, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 1],
        [2, 2, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 2, 2, 1, 2],
        [1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 2, 1, 1],
        [2, 2, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 1],
        [1, 2, 1, 2, 2, 2, 2, 1, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1],
        [1, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2],
        [1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 2, 1, 1, 2, 2, 1, 2],
        [2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1],
        [1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 2, 2],
        [1, 1, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1],
        [1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1],
        [2, 1, 2, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 2, 1, 2, 2],
        [1, 1, 1, 2, 2, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 1, 2, 1],
        [1, 2, 2, 1, 2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1],
        [2, 2, 1, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2],
        [1, 2, 2, 2, 1, 2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 2],
        [2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1],
        [1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 1, 2, 2, 1, 1, 2],
        [2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2]
    ]
))
    board.array_of_board_indices

    board1= GameBoard(3)
    print(board1.board)
    print()

