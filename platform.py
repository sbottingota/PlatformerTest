import pygame

from constants import *


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=DEFAULT_BLOCK_COLOR, solid=True, deadly=False):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.solid = solid
        self.deadly = deadly

    def update(self, *args, **kwargs):
        self.rect.x -= BLOCK_MOVE_AMOUNT
