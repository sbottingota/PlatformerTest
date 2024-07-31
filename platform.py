import pygame

from constants import *


class Block(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int,
                 color: str = DEFAULT_BLOCK_COLOR, solid: bool = True, deadly: bool = False, sticky: bool = False, level_end: bool = False):
        """
        Block object.
        :param x: The x position of the block.
        :param y: The y position of the block.
        :param width: The width of the block.
        :param height: The height of the block.
        :param color: The color of the block.
        :param solid: Whether the block is solid (defaults to True).
        :param deadly: Whether the block is deadly (defaults to False).
        :param sticky: Whether the block is sticky or not (defaults to False).
        :param level_end: Whether the block marks the end of the level (defaults to False).
        """
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self._relative_x = x

        self.solid = solid
        self.deadly = deadly
        self.sticky = sticky
        self.level_end = level_end

    def update(self, offset: int, *args, **kwargs) -> None:
        """
        Update the block.
        :param offset: The offset that the block should have from its original position.
        :return:
        """
        self.rect.x = self._relative_x - offset


class MovingBlock(Block):
    def __init__(self, x1: int, y1: int, x2: int, y2: int, width: int, height: int, move_speed: int = 0,
                 color: str = DEFAULT_BLOCK_COLOR, solid: bool = True, deadly: bool = False, sticky: bool = False, level_end: bool = False):
        """
        Moving block object.
        :param x1: The x coord of one of the endpoints of the block.
        :param y1: The y coord of one of the endpoints of the block.
        :param x2: The x coord of the other endpoint of the block.
        :param y2: The y coord of the other endpoint of the block.
        :param width: The width of the block.
        :param height: The height of the block.
        :param color: The color of the block.
        :param solid: Whether the block is solid (defaults to True).
        :param deadly: Whether the block is deadly (defaults to False).
        :param sticky: Whether the block is sticky or not (defaults to False).
        :param level_end: Whether the block marks the end of the level (defaults to False).
        """
        super().__init__(x1, y1, width, height, color, solid, deadly, sticky, level_end)

        self._x1 = x1
        self._y1 = y1

        self._x2 = x2
        self._y2 = y2

        self._move_speed = move_speed

        self._is_going_forward = True

    def update(self, offset: int, *args, **kwargs) -> None:
        super().update(offset)

        if self._is_going_forward:
            dest_x = self._x1
            dest_y = self._y1
        else:
            dest_x = self._x2
            dest_y = self._y2

        if abs(self._relative_x - dest_x) < self._move_speed \
                and abs(self.rect.y - dest_y) < self._move_speed:
            self._is_going_forward = not self._is_going_forward
        else:
            if self._relative_x > dest_x:
                self._relative_x -= self._move_speed
            else:
                self._relative_x += self._move_speed

            if self.rect.y > dest_y:
                self.rect.y -= self._move_speed
            else:
                self.rect.y += self._move_speed
