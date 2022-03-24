import pytest

from AlignFive import utils


@pytest.mark.parametrize(["func_input", "expected_value"],
     [
         [(20, [1, 5, 15]), [2]],
         [(1, [1, 2, 3]), [0]],
     ]
)
def test_find_index_of_closest_value(func_input, expected_value):
    click, allowed_positions = func_input
    closest_index = utils.find_index_of_closest_value(click, allowed_positions)

    assert closest_index == expected_value
