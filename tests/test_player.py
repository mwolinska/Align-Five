from AlignFive.players.human_player import Player
from AlignFive.utils import Color


test_list_of_players = [Player(1, Color(0, 0, 0)), Player(2, Color(255, 255, 255))]

# @pytest.mark.parametrize(["func_input", "expected_value"],
#     [
#         [(Player(1, Color(0, 0, 0)), test_list_of_players), test_list_of_players[1]],
#         [(Player(2, Color(255, 255, 255)), test_list_of_players), test_list_of_players[0]],
#     ]
# )
# def test_get_next_player(func_input, expected_value):
#     next_player = AlignFive.get_next_player(*func_input)
#
#     assert next_player == expected_value
