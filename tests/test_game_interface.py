import pytest

from AlignFive.utils import Click, Position
from tests.variables_for_tests import test_visual_0


@pytest.mark.parametrize(["func_input", "expected_value"],
    [
        [(test_visual_0, Click(200, 200)), Position(6, 6)],
        [(test_visual_0, Click(310, 155)), Position(4, 9)],
        [(test_visual_0, Click(30, 570)), Position(18, 0)],
    ]
 )
def test_translate_user_click_to_coords(func_input, expected_value):
    test_visual, user_click = func_input
    move_address = test_visual.translate_user_click_to_coords(user_click)

    assert move_address == expected_value



