import pygame

from constants import *


class Block(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int,
                 color: str = DEFAULT_BLOCK_COLOR, solid: bool = True, deadly: bool = False, level_end: bool = False):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.original_x = x

        self.solid = solid
        self.deadly = deadly
        self.level_end = level_end

    def update(self, offset: int, *args, **kwargs) -> None:
        self.rect.x = self.original_x - offset
