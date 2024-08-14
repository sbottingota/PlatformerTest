import pygame

from collections.abc import *

import level
from constants import *


class LevelSelector:
    def __init__(self, bg_color: str, level_filepaths: Sequence[str]):
        """
        Level selector object.
        :param bg_color: The background color of the level selector.
        :param level_filepaths: The level filepaths to select from.
        """
        self._bg_color = bg_color
        self._level_filepaths = level_filepaths

        button_bottom_spacing = WINDOW_SIZE[1] // (len(level_filepaths) // 2)
        self._buttons = []

        # left side
        self._buttons.extend([
            # 0.25 so that there is padding at the top too
            Button(BUTTON_SIDE_SPACING, (i + 0.25) * button_bottom_spacing, BUTTON_SIZE[0], BUTTON_SIZE[1],
                   f"Level {i + 1}", BUTTON_FONT, BUTTON_COLOR)
            for i in range(len(level_filepaths) // 2)])

        # right side
        self._buttons.extend([
            # 0.25 so that there is padding at the top too
            Button(WINDOW_SIZE[0] - (BUTTON_SIDE_SPACING + BUTTON_SIZE[0]), (i + 0.25) * button_bottom_spacing, BUTTON_SIZE[0], BUTTON_SIZE[1],
                   f"Level {(i + len(level_filepaths) // 2) + 1}", BUTTON_FONT, BUTTON_COLOR)
            for i in range(len(level_filepaths) // 2)
        ])

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self._bg_color)
        for button in self._buttons:
            button.draw(surface)

    def get_selected_level(self) -> level.Level | None:
        """
        :return: The selected level, or None if there isn't one.
        """
        for i, button in enumerate(self._buttons):
            if button.is_pressed():
                return level.parse_level(self._level_filepaths[i])

        return None


class Button:
    def __init__(self, x: float, y: float, width: float, height: float, text: str, font: pygame.font.Font, color: str):
        """
        Button object.
        :param x: The x coordinate of the button.
        :param y: The y coordinate of the button.
        :param width: The button's width.
        :param height: The button's height.
        :param text: The text on the button.
        :param font: The font of the button's text.
        :param color: The color of the button.
        """
        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        text_surface = font.render(text, True, "black")
        self.image.blit(text_surface,
                        ((width - text_surface.get_width()) / 2, (height - text_surface.get_height()) / 2))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def is_pressed(self) -> bool:
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(*pygame.mouse.get_pos())