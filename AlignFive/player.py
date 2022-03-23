from typing import List, TYPE_CHECKING


from AlignFive.utils import Color


class Player(object):
    def __init__(self, player_number: int, color: Color, is_random: bool = False):
        self.player_number = player_number
        self.color = color
        self.is_random = is_random

def get_next_player(player: Player, list_of_players: List[Player]) -> Player:
    if player.player_number == list_of_players[0].player_number:
        return list_of_players[1]
    else:
        return list_of_players[0]