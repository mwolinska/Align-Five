import logging
from typing import Tuple, List, Optional

import numpy as np

from AlignFive.interface.board import GameBoard
from AlignFive.players.abstract_player import AbstractPlayer
from AlignFive.players.human_player import Player
from AlignFive.players.smart_player import SmartPlayer
from AlignFive.data_model.move_data_model import Color, Position, Move


class AlignFive(object):

    def __init__(self,
         number_of_players: int = 2,
         with_bots: bool = False,
         generate_visual: bool = True,
         player_list: Optional[List[AbstractPlayer]] = None,
    ):
        self.number_of_players = number_of_players
        self.with_bots = with_bots
        self.game_board = GameBoard(generate_visual=generate_visual)

        if player_list is None:
            self.player_list = self.create_list_of_players()
        else:
            self.player_list = player_list

        self.player_index = 0

    @classmethod
    def from_existing_board(cls,
        current_game_state_board: np.ndarray,
        with_bots=False,
        generate_visual=False,
        player_list: Optional[List[AbstractPlayer]] = None,
    ):
        game = cls(with_bots=with_bots, generate_visual=False, player_list=player_list)
        game.game_board = GameBoard.from_array(current_game_state_board, generate_visual=generate_visual)
        if generate_visual:
            game.game_board.game_visual.from_existing_board(current_game_state_board)
        return game

    def create_list_of_players(self) -> List[AbstractPlayer]:
        list_of_players = []
        list_of_colors = [Color(0, 0, 0), Color(255, 255, 255)]
        player_number_counter = 1
        range_for_list = self.number_of_players
        if self.with_bots:
            range_for_list = self.number_of_players // 2

        for i in range(range_for_list):
            list_of_players.append(Player(player_number_counter, list_of_colors[i]))
            player_number_counter += 1
            if self.with_bots:
                list_of_players.append(SmartPlayer(player_number_counter, list_of_colors[i+1]))
                player_number_counter += 1

        return list_of_players

    def has_player_won(self, last_move: Move) -> bool:
        # possible win directions in order:[left, right], [up, down], [left top diagonal, right bottom diagonal],
        # [left bottom diagonal, right top diagonal]

        possible_win_directions = [
            [Position(0, -1), Position(0, 1)],
            [Position(-1, 0), Position(1, 0)],
            [Position(-1, -1), Position(1, 1)],
            [Position(1, -1), Position(-1, 1)],
        ]

        for dimension in possible_win_directions:
            stones_in_dimension = 0
            for direction in dimension:
                stones_in_dimension += self.game_board.count_neighbours(direction, last_move)

            if stones_in_dimension == 4:
                return True

        return False

    def is_game_draw(self) -> bool:
        if sum(self.game_board.available_positions_list) == 0:
            logging.info("The game is over, this is a draw")
            return True
        else:
            return False

    def is_game_over(self, last_move: Move) -> Tuple[bool, str]:

        if self.has_player_won(last_move):
            outcome_string = "Player " + str(last_move.player_number) + " won the game"
            return True, outcome_string
        else:
            if self.is_game_draw():
                outcome_string = "This game is a draw"
                return True, outcome_string
            else:
                outcome_string = "The game continues"
                return False, outcome_string

    def get_next_player(self) -> AbstractPlayer:
        player = self.player_list[self.player_index % self.number_of_players]
        return player

    def play_game(self):

        is_over = False
        outcome = None

        while not is_over:
            player = self.get_next_player()
            logging.debug(self.number_of_players)

            player_move = player.make_move(self.game_board)

            if player_move is None:
                is_over = True
                outcome = "Game ended early"
            elif self.game_board.is_position_available(player_move.position):
                self.game_board.game_visual.draw_stone(player_move.position, color=player.color)
                self.game_board.update_board(player_move)
                logging.debug(self.game_board.board)

                is_over, outcome = self.is_game_over(player_move)
                self.player_index += 1

            else:
                logging.info("Position is taken, try again")

        logging.info(outcome)

def single_player_game_main():
    logging.getLogger().setLevel(logging.INFO)
    my_game = AlignFive(with_bots=True)
    my_game.play_game()

def two_player_game_main():
    logging.getLogger().setLevel(logging.INFO)
    my_game = AlignFive()
    my_game.play_game()

if __name__ == '__main__':
    test_board = np.array([
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 0, 2, 1, 2, 1],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 0, 1, 2, 2],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    tic_tac_test = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    logging.getLogger().setLevel(logging.DEBUG)
    my_game = AlignFive.from_existing_board(test_board, generate_visual=True, with_bots=True)
    my_game.play_game()
