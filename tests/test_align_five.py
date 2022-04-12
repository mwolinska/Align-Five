import pytest

from AlignFive.game.align_five import AlignFive
from AlignFive.players.human_player import Player
from AlignFive.utils import Color, Position, Move
from tests.variables_for_tests import test_game, test_player_2, test_array_0, test_array_1, test_array_2


@pytest.mark.parametrize(["func_input", "expected_value"],
     [
        [test_game, [Player(1, Color(0, 0, 0)), Player(2, Color(255, 255, 255))]],
     ]
)
def test_create_list_of_players(func_input, expected_value):
    test_list_of_players = test_game.create_list_of_players()

    assert type(test_list_of_players) == type(expected_value)
    assert len(test_list_of_players) == len(expected_value)


@pytest.mark.parametrize(["func_input", "expected_value"],
     [
        [Move(Position(4, 3), test_player_2.player_number), True],
        [Move(Position(4, 13), test_player_2.player_number), True],
        [Move(Position(7, 3), test_player_2.player_number), False],
        [Move(Position(8, 9), test_player_2.player_number), False],
     ]
)
def test_has_player_won(func_input, expected_value):
    test_move = func_input
    is_win = AlignFive.from_existing_board(test_array_0).has_player_won(test_move)

    assert is_win == expected_value

@pytest.mark.parametrize(["func_input", "expected_value"],
     [
        [(test_game.from_existing_board(test_array_0)), False],
        [(test_game.from_existing_board(test_array_1)), True],
     ]
)
def test_is_game_draw(func_input, expected_value):
    is_draw = func_input.is_game_draw()

    assert is_draw == expected_value


@pytest.mark.parametrize(["func_input", "expected_value"],
    [
        [(test_game.from_existing_board(test_array_0), Move(Position(4, 3), test_player_2.player_number)), (True, "Player 2 won the game")],
        [(test_game.from_existing_board(test_array_0), Move(Position(0, 0), test_player_2.player_number)), (False, "The game continues")],
        [(test_game.from_existing_board(test_array_2), Move(Position(8, 9), test_player_2.player_number)), (True, "This game is a draw")],
    ]
 )
def test_is_game_over(func_input, expected_value):
    game, move = func_input
    is_over = game.is_game_over(move)

    assert is_over == expected_value
