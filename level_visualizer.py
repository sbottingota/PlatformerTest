from json import JSONDecodeError

import pygame

import level_selector
from constants import *
import level


class LevelVisualizer:
    def __init__(self, level_filepath: str, width: float, height: float, move_speed: float):
        self._level_filepath = level_filepath
        self._blocks = pygame.sprite.Group()

        self._offset_x = 0

        self._move_speed = move_speed

        self._reload_button = level_selector.Button(width * 8 / 10, height / 10, width / 10, height / 10, "Reload",
                                                    BUTTON_FONT, BUTTON_COLOR)

        self._load()

    def _load(self) -> None:
        self._blocks = pygame.sprite.Group(*level.parse_blocks(self._level_filepath))

    def update(self) -> None:
        if self._reload_button.is_pressed():
            self._load()

        if pygame.key.get_pressed()[KEYMAP.left]:
            self._offset_x -= self._move_speed

        if pygame.key.get_pressed()[KEYMAP.right]:
            self._offset_x += self._move_speed

        self._blocks.update(self._offset_x)

    def draw(self, screen: pygame.Surface):
        screen.fill(BACKGROUND_COLOR)
        self._blocks.draw(screen)
        self._reload_button.draw(screen)


def main() -> None:
    level_filepath = input("Enter level filepath: ")
    visualizer = LevelVisualizer(level_filepath, WINDOW_SIZE[0], WINDOW_SIZE[1], 10)

    screen = pygame.display.set_mode(WINDOW_SIZE)

    clock = pygame.time.Clock()

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        visualizer.update()
        visualizer.draw(screen)

        pygame.display.flip()

        clock.tick(60)


if __name__ == '__main__':
    main()
