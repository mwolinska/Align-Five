from AlignFive.align_five import AlignFive
from AlignFive.board import GameBoard
from AlignFive.game_interface import GameWindow
from AlignFive.player import Player
from AlignFive.utils import Color


# Test AligFive Game
from tests.arrays_for_tests import test_array_small, test_array_1, test_array_2, test_array_3, test_array_0

test_game = AlignFive()

# Test GameBoard
test_board = GameBoard()

test_board_0 = test_board.from_array(test_array_0)
test_board_1 = test_board.from_array(test_array_1)
test_board_2 = test_board.from_array(test_array_2)
test_board_3 = test_board.from_array(test_array_3)

test_board_small = test_board.from_array(test_array_small)

# Test players
test_player_1 = Player(1, Color(0, 0, 0))
test_player_2 = Player(2, Color(255, 255, 255))

# Test GameWindow
test_visual_0 = GameWindow()


