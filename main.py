import pygame

import level_selector
from constants import *
from player import State

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
running = True

selector = level_selector.LevelSelector(BACKGROUND_COLOR, ("levels/level_1.json", "levels/level_2.json"))
selected_level = None

is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    if selected_level is None:
        selected_level = selector.get_selected_level()
        selector.draw(screen)

    else:
        selected_level.update()
        selected_level.draw(screen)

        if selected_level.get_state() != State.PLAYING and pygame.key.get_pressed()[pygame.K_SPACE]:
            selected_level = None

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
