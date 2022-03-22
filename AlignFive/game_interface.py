from dataclasses import dataclass
from typing import Optional, Tuple, List

import pygame

from AlignFive.player import Player, get_next_player
from utils import find_index_of_closest_value, Position, Color

class GameWindow(object):
    def __init__(self,
                 width: int = 600,
                 height: int = 600,
                 n_horizontal_lines: int = 19,
                 n_vertical_lines: int = 19,):

        pygame.init()

        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode([self.width, self.height])

        self.symbol_size = None
        self.vertical_line_position_list = None
        self.horizontal_line_position_list = None
        self.x_position_grid_centre = None
        self.y_position_grid_centre = None
        self.x_symbol_centre = None
        self.y_symbol_centre = None

        self.n_horizontal_lines = n_horizontal_lines
        self.n_vertical_lines = n_vertical_lines

        self.prepare_board()

    def prepare_board(self):
        self.screen.fill((243, 197, 146))

        horizontal_margin = 0.05 * self.width
        vertical_margin = 0.05 * self.height
        board_width = self.width - 2 * horizontal_margin
        board_height = self.height - 2 * vertical_margin

        self.symbol_size = 0.22 * self.width / 3
        self.vertical_line_position_list = []
        self.horizontal_line_position_list = []

        number_of_columns = self.n_vertical_lines - 1

        # draw vertical lines. This corresponds to x values
        for i in range(number_of_columns + 1):
            start_pos = (horizontal_margin + i * board_width / number_of_columns, vertical_margin)
            end_pos = (horizontal_margin + i * board_width / number_of_columns, self.height - vertical_margin)
            pygame.draw.line(self.screen, (0, 0, 0), start_pos, end_pos)
            self.vertical_line_position_list.append(start_pos[0])


        for i in range(number_of_columns + 1):
            start_pos = (horizontal_margin, vertical_margin + i * board_height / number_of_columns)
            end_pos = (self.width - horizontal_margin, vertical_margin + i * board_height / number_of_columns)
            pygame.draw.line(self.screen, (0, 0, 0), start_pos, end_pos)
            self.horizontal_line_position_list.append(start_pos[1])

       # draw circles at selected position
        if self.n_vertical_lines == 19:
            circle_marking_line_indexes = [3, 9, 15]
            for x_el in circle_marking_line_indexes:
                x_coord = self.vertical_line_position_list[x_el]
                for y_el in circle_marking_line_indexes:
                    y_coord = self.horizontal_line_position_list[y_el]
                    pygame.draw.circle(self.screen,
                                               (0, 0, 0),
                                               (x_coord, y_coord),
                                               5,
                                       )
        pygame.display.flip()

    def get_user_interaction(self) -> Optional[Position]:
        running = True
        while running:

            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return Position(event.pos[0], event.pos[1])

        pygame.quit()
        return None

    def draw_stone(self, click: Position, color: Color):
        x_coord = find_index_of_closest_value(click.x, self.vertical_line_position_list)
        y_coord = find_index_of_closest_value(click.y, self.horizontal_line_position_list)

        pygame.draw.circle(
            self.screen, color.rgb,
            (self.vertical_line_position_list[x_coord], self.vertical_line_position_list[y_coord]), 20,
        )
        pygame.display.flip() # Updates board

if __name__ == '__main__':
    game_window = GameWindow(800, 800, 19, 19)
    players = [
        Player(1, Color(0, 0, 0)),
        Player(2, Color(255, 255, 255)),
    ]

    player = players[0]

    run_game = True
    while run_game:
        user_interaction = game_window.get_user_interaction()
        if user_interaction is None:
            run_game = False
        else:
            player = get_next_player(player, players)
            game_window.draw_stone(user_interaction, color=player.color)

    print("Game ended early")
    # game_window.get_user_interaction(1, -1)
    # game_window.game_outcome(0)

