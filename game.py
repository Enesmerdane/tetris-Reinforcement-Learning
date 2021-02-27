import pygame
import random

# GAME CONSTANTS
WINDOW_WIDTH  = 700
WINDOW_HEIGHT = 800 

BACKGROUND_COLOR = (200, 200, 255)

GAMESCREEN_WIDTH = 400
GAMESCREEN_HEIGHT = 600
GAMESCREEN_LOCATION_X = 50
GAMESCREEN_LOCATION_Y = 50

GAMESCREEN_COLOR = (150, 150, 255)

SCORE_LOCATION_X = 500
SCORE_LOCATION_Y = 50

#####################################################################################
def display_score(screen, score):
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, [SCORE_LOCATION_X, SCORE_LOCATION_Y])




#####################################################################################

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode( (WINDOW_HEIGHT, WINDOW_WIDTH) )

score = 0
font = pygame.font.SysFont(None, 35)


# start game
running = True
while running:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    screen.fill( BACKGROUND_COLOR )

    pygame.draw.rect(screen, GAMESCREEN_COLOR, [GAMESCREEN_LOCATION_X, GAMESCREEN_LOCATION_Y, GAMESCREEN_WIDTH, GAMESCREEN_HEIGHT])

    display_score(screen, score)

    pygame.display.update()

