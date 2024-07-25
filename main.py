import pygame

import platform
from constants import *

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
running = True

blocks = pygame.sprite.Group()
blocks.add(platform.Block(100, 620, 500, 100, BLOCK_COLOR))
blocks.add(platform.Block(600, 520, 200, 200, BLOCK_COLOR))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)
    blocks.update()
    blocks.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
