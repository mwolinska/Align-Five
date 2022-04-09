import abc
import dataclasses
import os
import random
import time
from dataclasses import dataclass
from itertools import repeat
from multiprocessing import Pool
from typing import Optional, List

from AlignFive.board import GameBoard
from AlignFive.game_sim import GameSim
from AlignFive.utils import Color, Position, Move


@dataclass
class PotentialMove:
    position: Position
    score: float

@dataclass
class PotentialMoves:
    potential_moves: List[PotentialMove] = dataclasses.field(default_factory=list)

    @property
    def best_potential_move(self) -> PotentialMove:
        try:
            best_move_score = self.potential_moves[0].score
            best_move = self.potential_moves[0]

            for potential_move in self.potential_moves:
                if potential_move.score > best_move_score:
                    best_move_score = potential_move.score
                    best_move = potential_move

            return best_move
        except IndexError:
            raise IndexError("Check your list before you wreck your list")


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
    def __init__(self, player_number: int, color: Color, n_workers: int = os.cpu_count(), n_simulations: int = 100):
        super().__init__()
        self.player_number = player_number
        self.color = color
        self.n_workers = n_workers
        # self.simulation_times = [[], []]
        self.n_simulations = n_simulations

    def make_move(self, board: GameBoard) -> Move:
        # tac = time.time()
        best_position = self.compute_best_position(board)
        # tic = time.time()
        # print(f"Elapsed time: {tic - tac}")
        best_move = Move(position=best_position, player_number=self.player_number)
        # self.simulation_times[0].append(board.available_positions_list.shape[0])
        # self.simulation_times[1].append((tic - tac))
        return best_move

    def simulate_move(self, position_index: int, board: GameBoard) -> PotentialMove:
        potential_position = Position.from_index(position_index, n_columns=board.board.shape[1])
        player_list = [RandomPlayer(2), RandomPlayer(1)]  # this player list needs to be generalised

        game = GameSim.from_existing_board(board.board, player_list)

        # Slow because runs all computations
        move_score = game.simulate(self.n_simulations, potential_position)

        return PotentialMove(position=potential_position, score=move_score)

    def compute_best_position(self, board: GameBoard) -> Optional[Position]:
        # best_move_score = 0
        # win_probability_array = np.ones([board.board.shape[0], board.board.shape[1]], dtype=float) * (- 1)

        fake_board = GameBoard.from_array(board.board.copy())
        iterative_arg = board.available_positions_list
        repeated_arg = fake_board

        with Pool(self.n_workers) as pool:
            list_potential_moves = pool.starmap(self.simulate_move, zip(iterative_arg, repeat(repeated_arg)))

        potential_moves = PotentialMoves(list_potential_moves)

        # for position_index in board.available_positions_list: # available_moves is the list of all possible moves for the Smart player at time T
        #
        #     potential_move = self.simulate_move(position_index, board)
        #
        #     potential_moves.potential_moves.append(potential_move)

        # get best move
        best_move = potential_moves.best_potential_move

        # win_probability_array[potential_position.row][potential_position.column] = move_score
        #
        # # Gets the best move
        # if move_score > best_move_score:
        #     best_move_score = move_score
        #     best_position = potential_position

        # board_probs = create_board_probs_from_list sjjhtd()
        # print(best_move.score)
        # print(win_probability_array.max())

        return best_move.position

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
