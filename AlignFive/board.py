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
    def __init__(self, board_size: int = 19):
        self.board = np.zeros((board_size, board_size))
        self.game_visual = GameWindow()

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, array_board: np.ndarray):
        self._board = array_board
        # self.board_size = array_board.shape

    @classmethod
    def from_array(cls, board: np.ndarray):
        game_board = cls()
        game_board.board = board
        return game_board

    def get_array_of_indices(self):
        list_of_indices = []
        for i in range(self.board.size):
            list_of_indices.append(i)

        return np.array(list_of_indices)

    def list_available_positions(self) -> List[int]:
        current_board = self.board.flatten()
        board_mask = current_board == 0
        list_of_board_indices = self.get_array_of_indices()

        return list_of_board_indices[board_mask]

    def is_position_available(self, move: Position) -> bool:
        available_positions = self.list_available_positions()
        position_index = move.row * self.board.shape[1] + move.column
        if position_index in available_positions:
            return True
        else:
            return False

    def select_random_position(self):

        available_position_selected = False
        available_positions_array = self.list_available_positions()

        while not available_position_selected:
            random_position = random.randint(0, (self.board.shape[0] * self.board.shape[1] - 1))

            if  random_position in available_positions_array:
                row_index = random_position // self.board.shape[1]
                column_index = random_position % self.board.shape[1]
                return row_index, column_index
            else:
                available_position_selected = False

    def update_board(self, move: Move):
        self.board[move.position.row][move.position.column] = move.player_number
        logging.debug(self.board)

    def count_neighbours(self, move_address: Position, check_direction: Position, player_number: int):

        is_neighbour_same_colour = True
        n_neighbouring_player_stones = 0
        next_field_increment = 1

        while is_neighbour_same_colour:
            next_row = move_address.row + (next_field_increment * check_direction.row)
            next_column = move_address.column + (next_field_increment * check_direction.column)

            if (next_row >= self.board.shape[0] or next_row < 0) or (next_column >= self.board.shape[1] or next_column < 0):
                return 0
            logging.debug(f"{next_row}, {next_column}")
            neighbour_value = self.board[next_row][next_column]

            if neighbour_value == player_number:
                n_neighbouring_player_stones += 1
                next_field_increment += 1
            else:
                is_neighbour_same_colour = False

        return n_neighbouring_player_stones

    # def select_best_position(self):
    #     current_game_board = self.board.copy()
    #     game_outcome_simulation = BoardSimulation(current_game_board)
    #     win_probability_matrix = game_outcome_simulation.simulate_possible_games()
    #     flat_win_probability_matrix = win_probability_matrix.flatten()
    #     possible_move_indexes = np.where(flat_win_probability_matrix == max(flat_win_probability_matrix))
    #     random.shuffle(possible_move_indexes)
    #     row = possible_move_indexes[0][0] // 3
    #     column = possible_move_indexes[0][0] % 3
    #     return row, column



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

