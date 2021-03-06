import os
from itertools import repeat
from multiprocessing import Pool
from typing import Optional

from AlignFive.interface.board import GameBoard
from AlignFive.game.game_sim import GameSim
from AlignFive.players.abstract_player import AbstractPlayer
from AlignFive.data_model.player_data_model import PotentialMove, PotentialMoves
from AlignFive.players.random_player import RandomPlayer
from AlignFive.data_model.move_data_model import Color, Move, Position


class SmartPlayer(AbstractPlayer):
    def __init__(self,
        player_number: int,
        color: Color,
        n_workers: int = int(os.environ.get("NUMBER_OF_WORKERS_TO_USE", default=os.cpu_count())),
        n_simulations: int = 100,
    ):
        super().__init__()
        self.player_number = player_number
        self.color = color
        self.n_workers = n_workers
        self.n_simulations = n_simulations

    def make_move(self, board: GameBoard) -> Move:
        best_position = self.compute_best_position(board)
        best_move = Move(position=best_position, player_number=self.player_number)

        return best_move

    def simulate_move(self, position_index: int, board: GameBoard) -> PotentialMove:
        potential_position = Position.from_index(position_index, n_columns=board.board.shape[1])
        player_list = [RandomPlayer(2), RandomPlayer(1)]  # this player list needs to be generalised

        game = GameSim.from_existing_board(board.board, player_list)

        # Slow because runs all computations
        move_score = game.simulate(self.n_simulations, potential_position)

        return PotentialMove(position=potential_position, score=move_score)

    def compute_best_position(self, board: GameBoard) -> Optional[Position]:
        fake_board = GameBoard.from_array(board.board.copy())
        iterative_arg = board.available_positions_list
        repeated_arg = fake_board

        with Pool(self.n_workers) as pool:
            list_potential_moves = pool.starmap(self.simulate_move, zip(iterative_arg, repeat(repeated_arg)))

        potential_moves = PotentialMoves(list_potential_moves)

        best_move = potential_moves.best_potential_move

        return best_move.position
