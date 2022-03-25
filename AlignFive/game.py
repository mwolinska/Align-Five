import logging
from typing import Tuple, List

from AlignFive.board import GameBoard
from AlignFive.player import Player, get_next_player, AbstractPlayer, RandomPlayer
from AlignFive.utils import Color, Position


class AlignFive(object):
    def __init__(self, number_of_players: int = 2, with_bots: bool = False):
        self.number_of_players = number_of_players
        self.with_bots = with_bots
        if self.with_bots:
            self.number_of_players = self.number_of_players // 2

        self.game_board = GameBoard()

    def create_list_of_players(self) -> List[AbstractPlayer]:
        list_of_players = []
        list_of_colors = [Color(0, 0, 0), Color(255, 255, 255)]

        for i in range(self.number_of_players):
            list_of_players.append(Player(i+1, list_of_colors[i]))
            if self.with_bots:
                list_of_players.append(RandomPlayer(i + 2, list_of_colors[i+1]))
        return list_of_players

    @staticmethod
    def has_player_won(current_board: GameBoard, move_player: AbstractPlayer, move_address: Position) -> bool:
        # possible win directions in order:
        # left, right,
        # up, down,
        # left top diagonal, right bottom diagonal,
        # left bottom diagonal, right top diagonal

        possible_win_directions = [[Position(0, -1), Position(0, 1)],
                                   [Position(-1, 0), Position(1, 0)],
                                   [Position(-1, -1), Position(1, 1)],
                                   [Position(1, -1), Position(-1, 1)],
       ]

        for dimension in possible_win_directions:
            stones_in_dimension = 0
            for direction in dimension:
                stones_in_dimension += current_board.count_neighbours(move_address, direction, move_player.player_number)

            if stones_in_dimension == 4:
                return True

        return False

    @staticmethod
    def is_game_draw(board: GameBoard) -> bool:
        if sum(board.list_available_position_indexes()) == 0:
            logging.info("The game is over, this is a draw")
            return True
        else:
            return False

    def is_game_over(self, board: GameBoard, player: Player, move_address: Position) -> Tuple[bool, str]:

        if self.has_player_won(board, player, move_address):
            outcome_string = "Player " + str(player.player_number) + " won the game"
            return True, outcome_string
        else:
            if self.is_game_draw(board):
                outcome_string = "This game is a draw"
                return True, outcome_string
            else:
                outcome_string = "The game continues"
                return False, outcome_string

    def play_game(self):
        player_list = self.create_list_of_players()
        player = player_list[0]

        is_over = False
        outcome = None

        while not is_over:

            player_move = player.make_move(self.game_board)

            if player_move is None:
                is_over = True
                outcome = "Game ended early"
            else:

                if self.game_board.is_position_available(player_move.position):
                    self.game_board.game_visual.draw_stone(player_move.position, color=player.color)
                    self.game_board.update_board(player_move)

                    is_over, outcome = self.is_game_over(self.game_board, player, player_move.position)
                    player = get_next_player(player, player_list)
                else:
                    logging.info("Position is taken, try again")

        logging.info(outcome)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    my_game = AlignFive(number_of_players=2, with_bots=True)
    my_game.play_game()
