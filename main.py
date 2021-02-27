import os
import sounds
import pygame as pg
from menu import Menu
from default_player import DefaultPlayer
from coop_player import CoopPlayer
from grid import Grid

text_color = (255, 255, 255)

# screen variables
min_screen_coord = (0, 0)
solo_max_screen_coord = (640, 720)
coop_max_screen_coord = (960, 720)
multiplayer_max_screen_coord = (1280, 720)
screen_res = solo_max_screen_coord
menu_coord = (screen_res[0] / 2, screen_res[1] / 4)

time_coord = (20, 200)
fps_coord = (20, 250)

FPS = 60
block_size = 30
glow_size = 25

display_fps = False
display_time = True

# key repeat
delay = 100  # milliseconds
interval = 50  # milliseconds

# game resources
font_file = 'SadanaSquare.ttf'


def write(font, message, color):
    text = font.render(str(message), True, color)
    text = text.convert_alpha()

    return text


def main():
    pg.init()
    pg.display.set_caption("Tetris")
    screen = pg.display.set_mode(solo_max_screen_coord)
    pg.key.set_repeat(delay, interval)

    normal_blocks_path = os.path.join('sprites', 'blocks.png')
    assist_blocks_path = os.path.join('sprites', 'assist_blocks.png')
    glow_blocks_path = os.path.join('sprites', 'glow_blocks.png')
    game_background_path = os.path.join('sprites', 'background.png')
    menu_background_path = os.path.join('sprites', 'background.png')
    grid_background_path = os.path.join('sprites', 'grid_background.png')

    # load backgrounds
    background_original = pg.image.load(game_background_path).convert()
    grid_background = pg.image.load(grid_background_path).convert()

    # load font
    font = pg.font.Font(os.path.join('fonts', font_file), 38)

    # load and scale all blocks (each tetromino has its own block color)
    def load_blocks(path, size, blocks_number):
        blocks_list = []
        blocks = pg.image.load(path).convert_alpha()
        blocks = pg.transform.scale(blocks, (size * blocks_number, size))
        for i in range(blocks_number):
            block_surface = blocks.subsurface(i * size, 0, size, size)
            blocks_list.append(block_surface)
        return blocks_list

    normal_blocks = load_blocks(normal_blocks_path, block_size, 8)
    assist_blocks = load_blocks(assist_blocks_path, block_size, 7)
    glow_blocks = load_blocks(glow_blocks_path, block_size + glow_size, 7)

    # (Left, Right, Rotate Clockwise, Rotate Counterclockwise, Drop, Speed Up)
    arrow_keys = (pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN, pg.K_SPACE, pg.K_RSHIFT)
    letter_keys = (pg.K_a, pg.K_d, pg.K_w, pg.K_s, pg.K_LSHIFT, pg.K_z)

    # create menu
    menu_items = ['SINGLE  PLAYER', 'MULTIPLAYER', 'CO-OP', 'QUIT']
    main_menu = Menu('TETRIS', menu_background_path, screen_res, font_file, menu_coord)
    for item in menu_items:
        main_menu.add_item(item)

    # when game_over is True return to main menu
    while True:
        display_menu = True
        multiplayer = False
        coop = False
        while display_menu:
            screen = pg.display.set_mode(solo_max_screen_coord)
            background = pg.transform.scale(background_original, screen.get_size())
            main_menu.show(screen)
            pg.display.flip()

            # wait for keyboard input
            event = pg.event.wait()
            user_input = main_menu.check_input(event)
            if user_input == menu_items[0]:  # single player
                display_menu = False
            elif user_input == menu_items[1]:  # multiplayer
                screen = pg.display.set_mode(multiplayer_max_screen_coord)
                background = pg.transform.scale(background_original, screen.get_size())
                multiplayer = True
                display_menu = False
            elif user_input == menu_items[2]:  # coop
                screen = pg.display.set_mode(coop_max_screen_coord)
                background = pg.transform.scale(background_original, screen.get_size())
                display_menu = False
                coop = True
            elif user_input == menu_items[3] or event.type == pg.QUIT:  # quit
                exit()

        player_list = []
        if not coop:
            left_player = DefaultPlayer(grid_background, block_size, (0, 0), solo_max_screen_coord)
            player_list.append(left_player)
        else:
            path = os.path.join('sprites', 'coop_grid_background.png')
            temp = pg.image.load(path).convert()

            grid = Grid(20, 20, block_size, coop_max_screen_coord, temp)
            left_player = CoopPlayer(grid, block_size, (0, 0), 0)
            right_player = CoopPlayer(grid, block_size, (0, 0), 1)
            player_list.append(left_player)
            player_list.append(right_player)
        if multiplayer:
            right_player = DefaultPlayer(grid_background, block_size,
                                         (multiplayer_max_screen_coord[0] // 2, 0),
                                         multiplayer_max_screen_coord)
            player_list.append(right_player)

        game_over = game_paused = False
        clock = pg.time.Clock()
        total_time = 0.0
        dt = 1.0 / FPS
        accumulator = 0.0

        while not game_over:
            # keyboard input
            for event in pg.event.get():
                if multiplayer or coop:
                    left_player.check_input(event, letter_keys)
                    right_player.check_input(event, arrow_keys)
                else:
                    left_player.check_input(event, arrow_keys)
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    game_over = True
                elif event.type == pg.KEYDOWN and event.key == pg.K_m:  # mute
                    sounds.mute = not sounds.mute
                    if sounds.mute:
                        pg.mixer.music.pause()
                    else:
                        pg.mixer.music.unpause()
                elif event.type == pg.KEYDOWN and event.key == pg.K_p:  # Pause the game
                    pause = True
                    sounds.pause_sound.play()
                    pg.mixer.music.pause()
                    for player in player_list:
                        player.display_message(screen, 'PAUSE')
                    pg.display.flip()
                    while pause:
                        event = pg.event.wait()
                        if event.type == pg.KEYDOWN and event.key == pg.K_p:
                            pause = False
                        elif event.type == pg.QUIT:
                            exit()
                    game_paused = True
                    pg.mixer.music.unpause()
                    sounds.pause_sound.play()

            if game_paused:
                frame_time = dt
                game_paused = False
                clock.tick(FPS)
            else:
                frame_time = clock.tick(FPS) / 1000.0  # convert to seconds

            # main game loop
            accumulator += frame_time
            while accumulator >= dt and not game_over:
                if multiplayer:
                    left_player.insert_lines(right_player.get_lines_cleared())
                    right_player.insert_lines(left_player.get_lines_cleared())
                elif coop:
                    # all players must have the same difficulty level
                    max_level = 0
                    for player in player_list:
                        if player.get_difficulty_level() > max_level:
                            max_level = player.get_difficulty_level()
                    for player in player_list:
                        if player.get_difficulty_level() != max_level:
                            player.increase_difficulty_level()
                for player in player_list:
                    player.main_loop(dt)
                    game_over = game_over or player.is_game_over()
                accumulator -= dt

            # create strings
            if display_time:
                total_time += frame_time
                time_string = "TIME " + '{0:02d}'.format(int(total_time // 60))\
                              + ":" + '{0:02d}'.format(int(total_time % 60))
                time_surface = write(font, time_string, text_color)
            if display_fps:
                fps_string = "FPS: " + str(int(clock.get_fps()))
                fps_surface = write(font, fps_string, text_color)

            # Draw
            screen.blit(background, min_screen_coord)
            if display_time:
                screen.blit(time_surface, time_coord)
            if display_fps:
                screen.blit(fps_surface, fps_coord)

            if coop:
                player_list[0].show_grid(screen, normal_blocks)
            for player in player_list:
                player.show(screen, normal_blocks, assist_blocks, glow_blocks)

            pg.display.flip()

        # end of game messages
        victory_color = (0, 255, 0)
        defeat_color = (255, 0, 0)
        tie_color = (255, 255, 0)
        tie = True
        # game over is True for all the players (tie)
        # game over is False for all the players (used escape to return to main menu)
        for player in player_list:
            tie = tie and player.is_game_over()
            game_over = game_over and not player.is_game_over()
        for player in player_list:
            if not multiplayer or (game_over and multiplayer):
                player.display_message(screen, 'GAME OVER', text_color)
            elif tie:
                player.display_message(screen, 'TIE', tie_color)
            elif player.is_game_over():
                player.display_message(screen, 'DEFEAT', defeat_color)
            else:
                player.display_message(screen, 'VICTORY', victory_color)
        pg.display.flip()
        pg.mixer.music.stop()
        clock.tick(0.7)


if __name__ == '__main__':
    main()
