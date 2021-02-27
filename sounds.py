import os
import pygame as pg

mute = False

pg.mixer.init()
menu_move_sound = pg.mixer.Sound(os.path.join('sounds', 'menu_move.wav'))
select_sound = pg.mixer.Sound(os.path.join('sounds', 'select.wav'))
pause_sound = pg.mixer.Sound(os.path.join('sounds', 'pause.wav'))
drop_sound = pg.mixer.Sound(os.path.join('sounds', 'drop.wav'))
clear_sound = pg.mixer.Sound(os.path.join('sounds', 'clear.wav'))
