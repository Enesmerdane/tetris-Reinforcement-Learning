from player import Player
from tetromino import Tetromino


class CoopPlayer(Player):

    def __init__(self, grid, block_size, viewport_min_coord, player_number):
        self.columns = (player_number * 10, (player_number + 1) * 10)
        # coordinates
        super().__init__(grid, block_size, viewport_min_coord, self.columns)
        # create next random tetromino
        self.next_tetromino_coord = (viewport_min_coord[0] + Player.next_tetromino_coord[0],
                                     viewport_min_coord[1] + Player.next_tetromino_coord[1] +
                                     3 * player_number * block_size)
        self.next_tetromino = Tetromino(self.randomizer.get_number(), block_size,
                                        self.next_tetromino_coord, self.tetromino_move_time)

    def get_difficulty_level(self):
        return self.difficulty_level

    def increase_difficulty_level(self):
        self.difficulty_level += 1
        self.tetromino_move_time *= Player.difficulty_modifier

    def show_grid(self, screen, normal_blocks):
        # blit text surfaces
        screen.blit(self.score_surface, self.lines_coord)
        screen.blit(self.level_surface, self.level_coord)
        screen.blit(self.next_surface, self.next_coord)
        self.grid.show(screen, normal_blocks)

    def show(self, screen, normal_blocks, assist_blocks, glow_blocks):
        # blit blocks
        if not self.grid.is_game_over():
            assist_coords = self.grid.get_assist_coords(self.current_tetromino.get_coords())
            for coord in assist_coords:
                screen.blit(assist_blocks[self.current_tetromino.get_color_index()], coord)
            self.current_tetromino.show(screen, normal_blocks, glow_blocks)
        self.next_tetromino.show(screen, normal_blocks, glow_blocks)
