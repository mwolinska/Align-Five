import numpy as np
import pytest

from AlignFive.utils import Position, Move
from tests.variables_for_tests import test_player_1, test_player_2, test_board, test_array_3, test_board_small, \
    test_board_3


@pytest.mark.parametrize(["func_input", "expected_value"],
    [
        [test_board_small, np.array([0, 1, 2, 6])],
    ]

)
def test_list_available_positions(func_input, expected_value):
    board_for_test = func_input
    test_list_of_indices = board_for_test.list_available_position_indexes()

    assert test_list_of_indices.all() == expected_value.all()


@pytest.mark.parametrize(["func_input", "expected_value"],
    [
        [(test_board_small, Position(0, 0)), True],
        [(test_board_small, Position(1, 1)), False],
    ]

)
def test_is_position_available(func_input, expected_value):
    board_for_test, test_move = func_input
    is_available = board_for_test.is_position_available(test_move)

    assert is_available == expected_value

# @pytest.mark.parametrize(["func_input", "expected_value"],
#     [
#         [test_board_small, (0, 2)]
#     ]
# )
# def test_select_random_position(func_input, expected_value):
#     random_index = func_input.select_random_position()
#     assert type(random_index) == type(expected_value)
#
#
@pytest.mark.parametrize(["func_input", "expected_value"],
    [
        [(test_board_small, Move(Position(0, 0), test_player_1.player_number)), np.array([[1, 0, 0], [1, 2, 1], [0, 2, 1]])],
        [(test_board_small, Move(Position(2, 0), test_player_2.player_number)), np.array([[0, 0, 0], [1, 2, 1], [2, 2, 1]])],
    ]
 )
def test_update_board(func_input, expected_value: np.ndarray):
    board_for_test, test_move = func_input
    test_board.update_board(test_move)

    assert board_for_test.board.all() == expected_value.all()

@pytest.mark.parametrize(["func_input", "expected_value"],
    [
        [(test_board_3, Position(0, -1), Move(Position(4, 3), test_player_2.player_number)), 2],
        [(test_board_small, Position(-1, -1), Move(Position(1, 1), test_player_2.player_number)), 0],
        [(test_board_small, Position(-1, -1), Move(Position(1, 1), test_player_2.player_number)), 0],

    ]
)
def test_count_neighbours(func_input, expected_value):
    board_for_test, check_dir, move = func_input
    n_neighbours_same_color = board_for_test.count_neighbours(check_dir, move)

    assert n_neighbours_same_color == expected_value
