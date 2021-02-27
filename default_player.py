from player import Player
from grid import Grid


class DefaultPlayer(Player):
    def __init__(self, grid_background, block_size, viewport_min_coord, viewport_max_coord):
        grid = Grid(Player.columns, Player.rows, block_size, viewport_max_coord, grid_background)
        super().__init__(grid, block_size, viewport_min_coord)
