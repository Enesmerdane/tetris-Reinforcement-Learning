import os
import sounds
import pygame as pg
from grid import Grid
from tetromino import Tetromino
from randomizer import BagRandomizer

font_file = 'SadanaSquare.ttf'


class Player:
    # game parameters
    text_color = (255, 255, 255)
    columns = 10
    rows = 20
    initial_move_time = 1  # time in seconds
    # difficulty -> move_time *= difficulty_modifier for every level
    difficulty_modifier = 0.85

    # text coordinates
    score_coord = (20, 50)
    lines_coord = (20, 100)
    level_coord = (20, 150)
    # next tetromino coordinates
    next_tetromino_coord = (64, 470)

    def __init__(self, grid, block_size, viewport_min_coord, columns=None):
        """
        :param grid: Grid object
        :param block_size: integer
        :param viewport_min_coord: (x, y)
        :param columns: (start, end) start <= column_index < end
        """
        self.randomizer = BagRandomizer(7)
        self.block_size = block_size
        self.difficulty_level = 1
        self.drop_tetromino = False

        # fonts
        self.game_font = pg.font.Font(os.path.join('fonts', font_file), 38)
        self.message_font = pg.font.Font(os.path.join('fonts', font_file), 50)

        # coordinates
        self.score_coord = (viewport_min_coord[0] + Player.score_coord[0],
                            viewport_min_coord[1] + Player.score_coord[1])
        self.level_coord = (viewport_min_coord[0] + Player.score_coord[0],
                            viewport_min_coord[1] + Player.score_coord[1])
        self.lines_coord = (viewport_min_coord[0] + Player.lines_coord[0],
                            viewport_min_coord[1] + Player.lines_coord[1])
        self.level_coord = (viewport_min_coord[0] + Player.level_coord[0],
                            viewport_min_coord[1] + Player.level_coord[1])
        self.next_tetromino_coord = (viewport_min_coord[0] + Player.next_tetromino_coord[0],
                                     viewport_min_coord[1] + Player.next_tetromino_coord[1])
        # next (text surface) coordinates
        self.next_coord = (self.next_tetromino_coord[0] - 10,
                           self.next_tetromino_coord[1] - 3 * block_size)

        self.columns = columns
        self.grid = grid
        self.tetromino_move_time = Player.initial_move_time
        # current random tetromino
        self.current_tetromino = Tetromino(self.randomizer.get_number(), block_size,
                                           self.grid.get_center_coord(self.columns),
                                           self.tetromino_move_time)
        # create next random tetromino
        self.next_tetromino = Tetromino(self.randomizer.get_number(), block_size,
                                        self.next_tetromino_coord, self.tetromino_move_time)

        self.next_surface = write(self.game_font, "NEXT", Player.text_color)
        self._create_strings()

    def check_input(self, event, keys):
        """
        :param event: pygame event
        :param keys: (left, right, rotate_cw, rotate_ccw, drop, speed up)
        """
        keys_pressed = pg.key.get_pressed()
        if event.type == pg.KEYDOWN:
            if keys_pressed[keys[0]]:
                self.current_tetromino.move_left()
                # if tetromino overlaps or it is out of bounds undo move left
                if self.grid.is_out_of_bounds(self.current_tetromino.get_coords(), self.columns) \
                        or self.grid.overlap(self.current_tetromino.get_coords()):
                    self.current_tetromino.move_right()
            elif keys_pressed[keys[1]]:
                self.current_tetromino.move_right()
                # if tetromino overlaps or it is out of bounds undo move right
                if self.grid.is_out_of_bounds(self.current_tetromino.get_coords(), self.columns) \
                        or self.grid.overlap(self.current_tetromino.get_coords()):
                    self.current_tetromino.move_left()

            if keys_pressed[keys[2]]:
                self.current_tetromino.rotate_cw()
                # if tetromino overlaps or it is out of bounds undo rotate clockwise
                if self.grid.is_out_of_bounds(self.current_tetromino.get_coords(), self.columns) \
                        or self.grid.overlap(self.current_tetromino.get_coords()):
                    self.current_tetromino.rotate_ccw()
            elif keys_pressed[keys[3]]:
                self.current_tetromino.rotate_ccw()
                # if tetromino overlaps or it is out of bounds undo rotate counterclockwise
                if self.grid.is_out_of_bounds(self.current_tetromino.get_coords(), self.columns) \
                        or self.grid.overlap(self.current_tetromino.get_coords()):
                    self.current_tetromino.rotate_cw()

            if keys_pressed[keys[4]]:  # drop the tetromino instantly
                if not sounds.mute:
                    sounds.drop_sound.play()
                self.drop_tetromino = True
            elif keys_pressed[keys[5]]:  # increase tetromino speed
                self.current_tetromino.speed_up()
        elif event.type == pg.KEYUP:  # reset tetromino speed
            if keys_pressed[keys[5]]:
                self.current_tetromino.reset_speed()

    def main_loop(self, dt):
        # drop tetromino (do move_down while self.drop_tetromino and not overlap)
        while True:
            self.current_tetromino.move_down(dt)
            overlap = self.grid.overlap(self.current_tetromino.get_coords())
            if not self.drop_tetromino or overlap:
                self.drop_tetromino = False
                break

        # tetromino overlaps a block or passed the bottom
        if overlap:
            while overlap and not self.grid.is_out_of_bounds(self.current_tetromino.get_coords(), self.columns):
                self.current_tetromino.move_up()
                overlap = self.grid.overlap(self.current_tetromino.get_coords())

            self.grid.update(self.current_tetromino.get_coords(), self.current_tetromino.get_color_index())
            # increase difficulty level every time 10 lines are cleared
            if self.grid.get_lines() // 10 + 1 != self.difficulty_level:
                self.difficulty_level += 1
                self.tetromino_move_time *= Player.difficulty_modifier

            # swap next and current tetromino and create a new tetromino
            self.current_tetromino = self.next_tetromino
            self.current_tetromino.set_coords(self.grid.get_center_coord(self.columns))
            self.current_tetromino.set_speed(self.tetromino_move_time)
            self.next_tetromino = Tetromino(self.randomizer.get_number(), self.block_size,
                                            self.next_tetromino_coord, self.tetromino_move_time)
        self._create_strings()

    def show(self, screen, normal_blocks, assist_blocks, glow_blocks):
        # blit text surfaces
        screen.blit(self.lines_surface, self.lines_coord)
        screen.blit(self.score_surface, self.score_coord)
        screen.blit(self.level_surface, self.level_coord)
        screen.blit(self.next_surface, self.next_coord)

        # blit blocks
        self.grid.show(screen, normal_blocks)
        if not self.grid.is_game_over():
            assist_coords = self.grid.get_assist_coords(self.current_tetromino.get_coords())
            for coord in assist_coords:
                screen.blit(assist_blocks[self.current_tetromino.get_color_index()], coord)
            self.current_tetromino.show(screen, normal_blocks, glow_blocks)
        self.next_tetromino.show(screen, normal_blocks, glow_blocks)

    def display_message(self, screen, text, color=text_color):
        self.grid.display_message(screen, self.message_font, color, text)

    def insert_lines(self, lines_number):
        self.grid.insert_blocks(lines_number)

    def get_lines_cleared(self):
        return self.grid.get_lines_cleared()

    def is_game_over(self):
        return self.grid.is_game_over()

    def _create_strings(self):
        score_string = "SCORE: " + str(self.grid.get_score())
        self.score_surface = write(self.game_font, score_string, Player.text_color)
        lines_string = "LINES: " + str(self.grid.get_lines())
        self.lines_surface = write(self.game_font, lines_string, Player.text_color)
        level_string = "LEVEL: " + str(self.difficulty_level)
        self.level_surface = write(self.game_font, level_string, Player.text_color)


def write(font, message, color):
    text = font.render(str(message), True, color)
    text = text.convert_alpha()
    return text
