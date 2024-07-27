import pygame

import game
from constants import *

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
running = True

level = game.parse_level("test_level.json")

while level.is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            level.is_running = False

    level.update()
    level.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
