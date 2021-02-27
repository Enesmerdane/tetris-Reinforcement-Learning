import pygame as pg
import sounds
from random import randint


class Grid:

    frames = 60
    lines_scores = [100, 250, 450, 800]  # scores for lines cleared

    def __init__(self, columns, rows, block_size, viewport_max_coord, background):
        """
        :param columns: number of columns
        :param rows: number of rows
        :param block_size: integer
        :param viewport_max_coord: (x, y)
        :param background: background image
        """
        self.lines = 0
        self.score = 0
        self.game_over = False
        self.lines_cleared = 0

        self.block_size = block_size

        self.area_width = columns * self.block_size
        self.area_height = rows * self.block_size

        # top left corner of the grid
        self.min_coord = ((viewport_max_coord[0] - self.area_width - 80),
                          (viewport_max_coord[1] - self.area_height) / 2)
        # bottom right corner of the grid
        self.max_coord = (self.min_coord[0] + self.area_width,
                          self.min_coord[1] + self.area_height)

        # center coord of the grid (tetromino start coord)
        self.center_coord = (self.min_coord[0] + (columns // 2) * self.block_size,
                             self.min_coord[1] + self.block_size)

        self.columns = columns
        self.rows = rows
        # rows x columns grid
        self.grid = [[-1 for i in range(self.columns)] for j in range(self.rows)]

        self.background = pg.transform.scale(background, (self.area_width, self.area_height))
        self.background.set_alpha(210)

    def overlap(self, tetromino_coords):
        """
        :param tetromino_coords: list of coordinates (x, y)
        :return: True if blocks overlap or passed the bottom
        """
        indexes_list = self._convert_coords(tetromino_coords)
        for row_index, column_index in indexes_list:
            if row_index >= self.rows or self.grid[row_index][column_index] >= 0:
                return True
        return False

    def is_out_of_bounds(self, tetromino_coords, columns=None):
        """
        :param tetromino_coords: list of coordinates (x, y)
        :param columns: (start, end) start <= column_index < end
        :return: True if a block is out of bounds or above the grid
        """
        if columns is None:
            x_min = self.min_coord[0]
            x_max = self.min_coord[0] + self.columns * self.block_size
        else:
            x_min = self.min_coord[0] + columns[0] * self.block_size
            x_max = self.min_coord[0] + columns[1] * self.block_size
        for x, y in tetromino_coords:
            if x > x_max - self.block_size or x < x_min or y < self.min_coord[1]:
                return True
        return False

    def is_game_over(self):
        return self.game_over

    def _convert_coords(self, coords):
        """
        Convert coordinates to grid indexes.
        :param coords: list of coordinates (x, y)
        :return: list of indexes (row_index, column_index)
        """
        indexes_list = []
        for coord in coords:
            column_index = int((coord[0] - self.min_coord[0]) // self.block_size)
            row_index = int((coord[1] - self.min_coord[1]) // self.block_size)
            indexes_list.append((row_index, column_index))
        return indexes_list

    def _convert_indexes(self, indexes):
        """
        Convert grid indexes to coordinates
        :param indexes: list of indexes (row_index, column_index)
        :return: list of coordinates (x, y)
        """
        coords_list = []
        for index in indexes:
            x = int(index[1] * self.block_size + self.min_coord[0])
            y = int(index[0] * self.block_size + self.min_coord[1])
            coords_list.append((x, y))
        return coords_list

    def update(self, coords, color_index):
        self.lines_cleared = 0
        """
        Converts coordinates to grid indexes and
        assigns color_index to the corresponding cells.
        :param coords: list of coordinates (x, y)
        :param color_index: tetromino color index
        """
        indexes_list = self._convert_coords(coords)
        for row_index, column_index in indexes_list:
            if row_index >= 0 and column_index >= 0:
                self.grid[row_index][column_index] = color_index

                # search for full rows
                if row_index == 0:  # there is a block at the first row
                    self.game_over = True

                full_row = True
                for j in range(self.columns):
                    if self.grid[row_index][j] == -1:  # cell is empty
                        full_row = False
                        break

                # delete the row if it is full
                if full_row:
                    self.lines_cleared += 1
                    del self.grid[row_index]
                    # insert a new line at the beginning of the grid
                    self.grid.insert(0, [-1 for i in range(self.columns)])

        self.lines += self.lines_cleared
        if self.lines_cleared:
            self.score += Grid.lines_scores[self.lines_cleared - 1]
            if not sounds.mute:
                sounds.clear_sound.play()

    def insert_blocks(self, lines):
        """
        Insert new lines at the end of the grid
        and remove the same number of lines at the top of the grid
        :param lines: number of lines
        """
        empty_column_index = randint(0, self.columns - 1)
        for i in range(lines):
            new_line = [7 for i in range(self.columns)]
            new_line[empty_column_index] = -1
            self.grid.pop(0)  # remove first line from the grid
            self.grid.append(new_line)  # insert the new line at the end of the grid

    def get_lines_cleared(self):
        """
        Return lines cleared and reset the variable
        :return: number of lines cleared
        """
        temp = self.lines_cleared
        self.lines_cleared = 0
        return temp

    def get_assist_coords(self, tetromino_coords):
        """
        :param tetromino_coords: list of coordinates (x, y)
        :return: coordinates of the assist blocks
        """
        indexes_list = self._convert_coords(tetromino_coords)
        bottom = False
        overlap = False

        # tetromino reached bottom
        for row_index, column_index in indexes_list:
            if row_index >= self.rows - 1:
                return tetromino_coords

        while not bottom and not overlap:
            # for every block
            for i in range(len(indexes_list)):
                row_index, column_index = indexes_list[i]
                indexes_list[i] = (row_index + 1, column_index)
                # check next row
                if self.grid[row_index + 1][column_index] >= 0:
                    overlap = True
                elif row_index + 1 >= self.rows - 1:
                    bottom = True

        if overlap:
            i = 0
            for row_index, column_index in indexes_list:
                indexes_list[i] = (row_index - 1, column_index)
                i += 1
        return self._convert_indexes(indexes_list)

    def show(self, screen, color_blocks):
        """
        Display background and all blocks.
        :param screen: screen surface
        :param color_blocks: block sprites tuple
        """
        screen.blit(self.background, self.min_coord)
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j] >= 0:  # if cell isn't empty (empty -> -1)
                    # cell value is color index
                    color_index = self.grid[i][j]
                    coord_x = self.min_coord[0] + j * self.block_size
                    coord_y = self.min_coord[1] + i * self.block_size
                    screen.blit(color_blocks[color_index], (coord_x, coord_y))

    def display_message(self, screen, font, color, message):
        text_surface = font.render(str(message), True, color).convert_alpha()
        text_x = self.min_coord[0] + (self.area_width - text_surface.get_width()) / 2
        text_y = (self.min_coord[1] + self.area_height) / 2
        screen.blit(text_surface, (text_x, text_y))

    def get_lines(self):
        return self.lines

    def get_score(self):
        return self.score

    def get_center_coord(self, columns=None):
        if columns is None:
            return self.center_coord
        else:
            return (self.min_coord[0] + columns[0] * self.block_size +
                    ((columns[1] - columns[0]) // 2) * self.block_size,
                    self.min_coord[1] + self.block_size)
