import pygame

from constants import *


class Block(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int,
                 color: str = DEFAULT_BLOCK_COLOR, solid: bool = True, deadly: bool = False, level_end: bool = False):
        """
        Block object.
        :param x: The x position of the block.
        :param y: The y position of the block.
        :param width: The width of the block.
        :param height: The height of the block.
        :param color: The color of the block.
        :param solid: Whether the block is solid (defaults to True).
        :param deadly: Whether the block is deadly (defaults to False).
        :param level_end: Whether the block marks the end of the level (defaults to False).
        """
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self._original_x = x

        self.solid = solid
        self.deadly = deadly
        self.level_end = level_end

    def update(self, offset: int, *args, **kwargs) -> None:
        """
        Update the block.
        :param offset: The offset that the block should have from its original position.
        :return:
        """
        self.rect.x = self._original_x - offset
