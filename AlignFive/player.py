import abc
import logging
import random
from typing import Tuple, Optional

from AlignFive.board import GameBoard
from AlignFive.game_sim import GameSim
from AlignFive.utils import Color, Position, Move


class AbstractPlayer(abc.ABC):
    def __init__(self):
        self.player_number = None
        self.color = None
    @abc.abstractmethod
    def make_move(self, board: GameBoard) -> Move:
        pass

class Player(AbstractPlayer):
    def __init__(self, player_number: int, color: Color):
        super().__init__()
        self.player_number = player_number
        self.color = color

    def make_move(self, board: GameBoard) -> Optional[Move]:
        user_interaction = board.game_visual.get_user_interaction()
        if user_interaction is None:
            return None
        else:
            move_address = board.game_visual.translate_user_click_to_coords(user_interaction)
        return Move(position=move_address, player_number=self.player_number)

class RandomPlayer(AbstractPlayer):
    def __init__(self, player_number: int, color: Color = Color(0, 0, 0)):
        super().__init__()
        self.player_number = player_number
        self.color = color

    @staticmethod
    def select_random_position(board: GameBoard) -> Position:
        random_position_index = random.choice(board.available_positions_list)
        random_position = Position.from_index(random_position_index, board.board.shape[1])
        return random_position

    def make_move(self, board: GameBoard) -> Move:
        random_position = self.select_random_position(board)
        return Move(random_position, player_number=self.player_number)

class SmartPlayer(AbstractPlayer):
    def __init__(self, player_number: int, color: Color):
        super().__init__()
        self.player_number = player_number
        self.color = color

    def make_move(self, board: GameBoard) -> Move:
        best_position = self.compute_best_position(board)
        best_move = Move(position=best_position, player_number=self.player_number)
        return best_move

    def compute_best_position(self, board: GameBoard, number_of_simulations: int = 50) -> Optional[Position]:
        best_move_score = 0

        player_list = [RandomPlayer(2), RandomPlayer(1)] # this player list needs to be generlaised

        for position_index in board.available_positions_list: # available_moves is the list of all possible moves for the Smart player at time T

            potential_position = Position.from_index(position_index, n_columns=board.board.shape[1])

            fake_board = GameBoard.from_array(board.board.copy())
            game = GameSim.from_existing_board(fake_board.board, player_list)

            move_score = game.simulate(number_of_simulations, potential_position)

            if move_score > best_move_score:
                best_move_score = move_score
                best_position = potential_position

        return best_position

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