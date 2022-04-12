from AlignFive.interface.board import GameBoard
from AlignFive.players.abstract_player import AbstractPlayer
from AlignFive.utils import Move


class AllKnowingPlayer(AbstractPlayer):
    def __init__(self):
        pass

    def make_move(self, board: GameBoard) -> Move:
        pass
