import pygame

import level
from constants import *


class LevelSelector:
    def __init__(self, bg_color, level_filepaths):
        self.bg_color = bg_color
        self.level_filepaths = level_filepaths
        self.current_level = None

        button_bottom_spacing = WINDOW_SIZE[1] // len(level_filepaths)
        self.buttons = [
            Button(BUTTON_LEFT_SPACING, i * button_bottom_spacing, BUTTON_SIZE[0], BUTTON_SIZE[1],
                   f"Label {i}", BUTTON_FONT, BUTTON_COLOR)
            for i in range(len(level_filepaths))]

    def draw(self, surface):
        surface.fill(self.bg_color)
        for button in self.buttons:
            button.draw(surface)

    def get_selected_level(self):
        for i, button in enumerate(self.buttons):
            if button.is_pressed():
                return level.parse_level(self.level_filepaths[i])

        return None


class Button:
    def __init__(self, x, y, width, height, text, font, color):
        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        text_surface = font.render(text, True, "black")
        self.image.blit(text_surface,
                        ((width - text_surface.get_width()) / 2, (height - text_surface.get_height()) / 2))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def is_pressed(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(*pygame.mouse.get_pos())