import random
from typing import List, Tuple

import numpy as np

from AlignFive.player import Player
from AlignFive.utils import Position


class GameBoard(object):
    def __init__(self, board_size: int = 19):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size))

    def list_available_positions(self) -> List[bool]:
        current_board = self.board.flatten()
        board_mask = current_board == 0
        return board_mask

    def is_position_available(self, move: Position) -> bool:
        available_positions = self.list_available_positions()
        position_index = move.row * self.board_size + move.column
        return available_positions[position_index]

    def select_random_position(self):

        available_position_selected = False
        available_positions_list = self.list_available_positions()

        while not available_position_selected:
            random_position = random.randint(0, (self.board_size * self.board_size - 1))

            if available_positions_list[random_position]:
                row_index = random_position // self.board_size
                column_index = random_position % self.board_size
                return row_index, column_index
            else:
                available_position_selected = False

    def update_board(self, move: Position, player: Player):
        self.board[move.row][move.column] = player.player_number
        print(self.board)

    def get_board_subset_for_eval(self, move: Position):
        move_nearest_neighbours = self.board[(move.row - 1):(move.row + 2), (move.column - 1):(move.column + 2)]
        mask = move_nearest_neighbours ==
        print(a)


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



