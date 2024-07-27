import pygame

import platform
import player
from constants import *

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
running = True

blocks_group = pygame.sprite.Group()
blocks_group.add(platform.Block(100, 620, 500, 100, BLOCK_COLOR))
blocks_group.add(platform.Block(600, 520, 200, 200, BLOCK_COLOR))
blocks_group.add(platform.Block(800, 420, 300, 300, BLOCK_COLOR))

player_group = pygame.sprite.GroupSingle(player.Player(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2, PLAYER_SIZE, PLAYER_COLOR, 20, 1))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    screen.fill(BACKGROUND_COLOR)
    blocks_group.update()
    blocks_group.draw(screen)

    player_group.update(blocks_group.sprites(), keys[pygame.K_SPACE])
    player_group.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
