import os

import pygame

import level_selector
from constants import *
from player import State


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    selector = level_selector.LevelSelector(BACKGROUND_COLOR, [f"./levels/{file}" for file in sorted(os.listdir("./levels/"))])
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

            if selected_level.state != State.PLAYING and pygame.key.get_pressed()[KEYMAP.skip]:
                selected_level = None

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
