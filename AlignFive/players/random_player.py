import random

from AlignFive.interface.board import GameBoard
from AlignFive.players.abstract_player import AbstractPlayer
from AlignFive.data_model.move_data_model import Color, Position, Move


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
