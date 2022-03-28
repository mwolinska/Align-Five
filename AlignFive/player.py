import abc
import random
from typing import List, Tuple, Optional

from AlignFive.board import GameBoard
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
    def __init__(self, player_number: int, color: Color):
        super().__init__()
        self.player_number = player_number
        self.color = color

    @staticmethod
    def select_random_position(board: GameBoard) -> Tuple[int, int]:
        available_position_selected = False
        available_positions_list = board.list_available_position_indexes()

        while not available_position_selected:
            random_position = random.randint(0, ((board.board.shape[0] * board.board.shape[1]) - 1))

            if available_positions_list[random_position]:
                row_index = random_position // board.board.shape[1]
                column_index = random_position % board.board.shape[1]
                return row_index, column_index
            else:
                available_position_selected = False

    def make_move(self, board: GameBoard) -> Move:
        random_position = self.select_random_position(board)
        return Move(position=Position.from_tuple(random_position), player_number=self.player_number)

def get_next_player(player: Player, list_of_players: List[AbstractPlayer]) -> Player:
    if player.player_number == list_of_players[0].player_number:
        return list_of_players[1]
    else:
        return list_of_players[0]