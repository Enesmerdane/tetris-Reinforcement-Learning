import pygame
import random

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode( (800, 700) )

running = True
while running:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    screen.fill( (200, 200, 255) )

    pygame.draw.rect(screen, (150, 150, 255), [50, 50, 400, 600])

    pygame.display.update()


    