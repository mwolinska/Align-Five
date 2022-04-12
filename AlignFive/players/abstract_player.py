import abc

from AlignFive.interface.board import GameBoard
from AlignFive.data_model.move_data_model import Move


class AbstractPlayer(abc.ABC):
    def __init__(self):
        self.player_number = None
        self.color = None
    @abc.abstractmethod
    def make_move(self, board: GameBoard) -> Move:
        pass
