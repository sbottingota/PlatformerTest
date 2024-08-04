import enum
from collections.abc import *

import pygame

import platform
from constants import *


class State(enum.Enum):
    PLAYING = 0
    FAILED = 1
    COMPLETED = 2


class Direction(enum.Enum):
    LEFT = 0
    RIGHT = 1


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int | float, y: int | float, size: int | float, color: str, move_speed: int | float,
                 jump_strength: int | float, acceleration: int | float, gravity: int | float,
                 *groups: pygame.sprite.Group):
        """
        Player object.
        :param x: The x coordinate for the player.
        :param y: The initial y coordinate for the player.
        :param size: The size of the player.
        :param color: The color of the player.
        :param move_speed: The maximum speed that the player can move (pixels per loop).
        :param jump_strength: The strength of the player's jump (pixels per loop of initial jump momentum).
        :param acceleration: The player's lateral acceleration/deceleration speed (pixels per loop, per loop).
        :param gravity: The strength of gravity (pixels per loop).
        :param groups: Any groups that the player is in.
        """
        super().__init__(*groups)

        self.image = pygame.Surface((size, size))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self._move_speed = move_speed
        self._jump_strength = jump_strength
        self._acceleration = acceleration
        self._gravity = gravity

        self.state = State.PLAYING

        self._dx = 0
        self._dy = 0

        self.x_offset = 0

    def update(self, blocks: Collection[platform.Block], move: Direction | None = None, jump: bool = False, *args, **kwargs) -> None:
        """
        Update the player.
        :param blocks: The blocks in the level (to check collisions, etc.)
        :param move: The direction to move, or None if the player should not move.
        :param jump: Whether to jump or not
        """
        # handle collisions with blocks with certain attributes
        if self._check_collision_from_predicate(lambda block: block.deadly, blocks):
            self.state = State.FAILED

        if self._check_collision_from_predicate(lambda block: block.level_end, blocks):
            self.state = State.COMPLETED

        if self._check_collision_from_predicate(lambda block: block.sticky, blocks):
            jump = False

        # handle side collisions
        side_collisions = self._check_side_collision(self._move_speed + 1, blocks)
        if side_collisions == Direction.RIGHT:
            self.x_offset -= PLAYER_DISLODGE_STRENGTH

        elif side_collisions == Direction.LEFT:
            self.x_offset += PLAYER_DISLODGE_STRENGTH

        else:
            self.x_offset += self._dx

        # handle bottom collisions and jumping
        if self._check_bottom_collision(self._dy + 1, blocks):
            if jump:
                self._dy = -self._jump_strength
            else:
                self.rect.y -= self._dy
                self._dy = 0

        else:
            self._dy += self._gravity

        # handle movement
        if abs(self._dx) < self._move_speed:
            if move == Direction.LEFT:
                self._dx -= self._acceleration
            elif move == Direction.RIGHT:
                self._dx += self._acceleration
        if abs(self._dx > self._move_speed) or move is None:
            if self._dx > 0:
                self._dx -= self._acceleration

            elif self._dx < 0:
                self._dx += self._acceleration

        # update y pos
        self.rect.y += self._dy

    def _check_side_collision(self, collision_limit: int, blocks: Collection[platform.Block]) -> Direction | None:
        """
        Check for side collisions.
        :param collision_limit: The limit to the difference between the positions of the corresponding edges.
        :param blocks: The blocks in the level.
        :return: A Direction corresponding with what side collided with the player, or None if no collisions.
        """
        for block in blocks:
            if block.solid and self.rect.colliderect(block.rect):
                if self.rect.right >= block.rect.left > self.rect.right - collision_limit:
                    return Direction.RIGHT

                elif self.rect.left <= block.rect.right < self.rect.left + collision_limit:
                    return Direction.LEFT

        return None

    def _check_bottom_collision(self, collision_limit: int, blocks: Collection[platform.Block]) -> bool:
        """
        Check for bottom collisions.
        :param collision_limit: The limit to the difference between the positions of the corresponding edges.
        :param blocks: The blocks in the level.
        :return: Whether there is a bottom collision.
        """
        for block in blocks:
            if block.solid and self.rect.colliderect(block.rect):
                if block.rect.top <= self.rect.bottom < block.rect.top + collision_limit:
                    return True
        return False

    def _check_collision_from_predicate(self, predicate: Callable[[platform.Block], bool],
                                        blocks: Collection[platform.Block]) -> bool:
        """
        Checks for collisions based on a given predicate.
        :param predicate: The condition to filter blocks by.
        :param blocks: the blocks in the level.
        :return: Whether a specified collision exists.
        """
        return any(self.rect.colliderect(block) for block in blocks if predicate(block))
