import random
from random import randint
from typing import Tuple

import numpy as np

from AlignFive.board import GameBoard
from AlignFive.game_interface import GameWindow
from AlignFive.player import Player, get_next_player
from AlignFive.utils import Color, Position


class AlignFive(object):
    def __init__(self, number_of_human_players: int = 2, number_of_random_players: int = 0):
        self.number_of_human_players = number_of_human_players
        self.number_of_random_players = number_of_random_players

    def create_list_of_players(self):
        list_of_players = []
        list_of_colors = [Color(0, 0, 0), Color(255, 255, 255)]

        for i in range(self.number_of_human_players):
            list_of_players.append(Player(i+1, list_of_colors[i], False))

        # for i in range(self.number_of_random_players):
        #     list_of_players.append(Player(i+2, True))

        return list_of_players

    def has_player_won(self, current_board: GameBoard, move_player: Player, move_address: Position) -> bool:

        board_subset_for_eval = current_board.board[(move_address.row - 2):(move_address.row + 3), (move_address.column - 2):(move_address.column + 3)]
        print(board_subset_for_eval)

        is_win_mask = board_subset_for_eval == move_player.player_number

        for i in range(5):
            # is there a win in each row?
            if np.all(is_win_mask[:, i]):
                print("Player " + str(move_player.player_number) + " has won the game")
                return True
            # is there a win in each column?
            elif np.all(is_win_mask[i, :]):
                print("Player " + str(move_player.player_number) + " has won the game")
                return True
        # Check if there is a win across the diagonals
        # if is_win_mask[0][0] == is_win_mask[1][1] == is_win_mask[2][2] == True:
        #     return True
        # elif is_win_mask[2][0] == is_win_mask[1][1] == is_win_mask[0][2] == True:
        #     return True

        return False

    def is_game_draw(self, board: GameBoard) -> bool:
        if sum(board.list_available_positions()) == 0:
            print("The game is over, this is a draw")
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
        game_visual = GameWindow()
        game_board = GameBoard()
        player_list = self.create_list_of_players()
        player = player_list[0]

        is_over = False
        outcome = None

        while not is_over:
            user_interaction = game_visual.get_user_interaction()

            if user_interaction is None:
                is_over = True
                outcome = "Game ended early"
            else:
                move_address = game_visual.translate_user_click_to_coords(user_interaction)

                if game_board.is_position_available(move_address):
                    game_visual.draw_stone(move_address, color=player.color)
                    game_board.update_board(move_address, player)
                    is_over, outcome = self.is_game_over(game_board, player, move_address)
                    player = get_next_player(player, player_list)
                else:
                    print("Position is taken, try again")

        print(outcome)

if __name__ == '__main__':
    my_game = AlignFive()
    my_game.play_game()