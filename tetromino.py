import os
import pygame as pg


class Tetromino:
    # I tetromino
    i_tetromino_angle_0 = ["....",
                           "####",
                           "....",
                           "...."]

    # rotate 90 degrees cw (clockwise)
    i_tetromino_angle_90 = [".#..",
                            ".#..",
                            ".#..",
                            ".#.."]

    i_tetromino = (i_tetromino_angle_0, i_tetromino_angle_90,
                   i_tetromino_angle_0, i_tetromino_angle_90)

    # O tetromino
    o_tetromino_angle_0 = ["##..",
                           "##..",
                           "....",
                           "...."]

    o_tetromino = (o_tetromino_angle_0, o_tetromino_angle_0,
                   o_tetromino_angle_0, o_tetromino_angle_0)

    # T tetromino
    t_tetromino_angle_0 = [".#..",
                           "###.",
                           "....",
                           "...."]

    # rotate 90 degrees cw
    t_tetromino_angle_90 = [".#..",
                            ".##.",
                            ".#..",
                            "...."]

    # rotate 180 degrees cw
    t_tetromino_angle_180 = ["....",
                             "###.",
                             ".#..",
                             "...."]

    # rotate 270 degrees cw
    t_tetromino_angle_270 = [".#..",
                             "##..",
                             ".#..",
                             "...."]

    t_tetromino = (t_tetromino_angle_0, t_tetromino_angle_90,
                   t_tetromino_angle_180, t_tetromino_angle_270)

    # J tetromino
    j_tetromino_angle_0 = ["#...",
                           "###.",
                           "....",
                           "...."]

    # rotate 90 degrees cw
    j_tetromino_angle_90 = [".##.",
                            ".#..",
                            ".#..",
                            "...."]

    # rotate 180 degrees cw
    j_tetromino_angle_180 = ["....",
                             "###.",
                             "..#.",
                             "...."]

    # rotate 270 degrees cw
    j_tetromino_angle_270 = [".#..",
                             ".#..",
                             "##..",
                             "...."]

    j_tetromino = (j_tetromino_angle_0, j_tetromino_angle_90,
                   j_tetromino_angle_180, j_tetromino_angle_270)

    # L tetromino cw
    l_tetromino_angle_0 = ["..#.",
                           "###.",
                           "....",
                           "...."]

    # rotate 90 degrees cw
    l_tetromino_angle_90 = [".#..",
                            ".#..",
                            ".##.",
                            "...."]

    # rotate 180 degrees cw
    l_tetromino_angle_180 = ["....",
                             "###.",
                             "#...",
                             "...."]

    # rotate 270 degrees cw
    l_tetromino_angle_270 = ["##..",
                             ".#..",
                             ".#..",
                             "...."]

    l_tetromino = (l_tetromino_angle_0, l_tetromino_angle_90,
                   l_tetromino_angle_180, l_tetromino_angle_270)

    # S tetromino
    s_tetromino_angle_0 = [".##.",
                           "##..",
                           "....",
                           "...."]

    # rotate 90 degrees cw
    s_tetromino_angle_90 = [".#..",
                            ".##.",
                            "..#.",
                            "...."]

    s_tetromino = (s_tetromino_angle_0, s_tetromino_angle_90,
                   s_tetromino_angle_0, s_tetromino_angle_90)

    # Z tetromino
    z_tetromino_angle_0 = ["##..",
                           ".##.",
                           "....",
                           "...."]

    # rotate 90 degrees cw
    z_tetromino_angle_90 = ["..#.",
                            ".##.",
                            ".#..",
                            "...."]

    z_tetromino = (z_tetromino_angle_0, z_tetromino_angle_90,
                   z_tetromino_angle_0, z_tetromino_angle_90)

    tetrominoes = (i_tetromino, o_tetromino, t_tetromino, j_tetromino,
                   l_tetromino, s_tetromino, z_tetromino)

    fast_move_time = 0.03  # seconds

    def __init__(self, index, block_size, coord, move_time):
        """
        :param index: 0 - 6 (I, O, T, J, L, S, Z)
        :param block_size: integer
        :param coord: (x, y)
        :param move_time: time in seconds
        """
        self.tetromino_index = index
        self.random_tetromino = Tetromino.tetrominoes[self.tetromino_index]

        self.current_angle = 0
        self.current_frame = self.random_tetromino[self.current_angle]

        self.block_size = block_size

        # coordinates of the center block (required for the rotation)
        self.center_coord = list(coord)

        # coordinates for each block of the tetromino
        # list of coordinates [x, y]
        self.blocks_coords = self._build()

        # time in seconds
        self.normal_move_time = move_time
        self.move_time = self.normal_move_time
        self.elapsed_time = 0.0

    def _build(self):
        """
        Calculates the coordinates of each block that is part of the tetromino.
        center block index is (1, 1)
        :return: list of coordinates [x, y] or empty list if a block is out of bounds
        """
        x, y = [self.center_coord[0] - self.block_size, self.center_coord[1]
                - self.block_size]
        tetromino_coords = []

        for i in range(len(self.current_frame)):
            for char in self.current_frame[i]:
                if char == '#':
                    tetromino_coords.append([x, y])
                x += self.block_size
            x = self.center_coord[0] - self.block_size
            y += self.block_size
        return tetromino_coords

    def set_coords(self, center_coord):
        self.center_coord = list(center_coord)
        self.blocks_coords = self._build()

    def get_coords(self):
        return self.blocks_coords

    def get_color_index(self):
        return self.tetromino_index

    def speed_up(self):
        self.move_time = Tetromino.fast_move_time

    def reset_speed(self):
        self.move_time = self.normal_move_time

    def set_speed(self, move_time):
        self.normal_move_time = move_time
        self.move_time = self.normal_move_time

    def show(self, screen, color_blocks, glow_blocks):
        """
        Display all blocks.
        :param screen: screen surface
        :param color_blocks: block surfaces tuple
        :param glow_blocks: glow block surfaces tuple
        """
        offset = abs(self.block_size - glow_blocks[0].get_width()) // 2
        for coord in self.blocks_coords:
            screen.blit(glow_blocks[self.tetromino_index], (coord[0] - offset,
                                                            coord[1] - offset))
            screen.blit(color_blocks[self.tetromino_index], coord)

    def move_up(self):
        for coord in self.blocks_coords:
            coord[1] -= self.block_size
        self.center_coord[1] -= self.block_size

    def move_down(self, time):
        """
        Move down all blocks.
        """
        self.elapsed_time += time
        if self.elapsed_time >= self.move_time:
            self.elapsed_time = 0
            for coord in self.blocks_coords:
                coord[1] += self.block_size
            self.center_coord[1] += self.block_size

    def move_left(self):
        """
        Move left all blocks.
        """
        self.center_coord[0] -= self.block_size
        for coord in self.blocks_coords:
            coord[0] -= self.block_size

    def move_right(self):
        """
        Move right all blocks.
        """
        self.center_coord[0] += self.block_size
        for coord in self.blocks_coords:
            coord[0] += self.block_size

    def rotate_ccw(self):
        """
        Rotate the tetromino 90 degrees counterclockwise.
        """
        if self.current_angle == 0:
            self.current_angle = 3
        else:
            self.current_angle -= 1

        self.current_frame = self.random_tetromino[self.current_angle]
        self.blocks_coords = self._build()

    def rotate_cw(self):
        """
        Rotate the tetromino 90 degrees clockwise.
        """
        self.current_angle = (self.current_angle + 1) % 4
        self.current_frame = self.random_tetromino[self.current_angle]
        self.blocks_coords = self._build()
