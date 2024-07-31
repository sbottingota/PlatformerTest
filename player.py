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
    NONE = 0
    LEFT = 1
    RIGHT = 2


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, size: int, color: str, move_speed: int, jump_strength: int, gravity: int,
                 *groups: pygame.sprite.Group):
        super().__init__(*groups)

        self.image = pygame.Surface((size, size))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.move_speed = move_speed
        self.jump_strength = jump_strength
        self.gravity = gravity

        self.state = State.PLAYING

        self.dx = 0
        self.dy = 0

        self.x_offset = 0

    def update(self, blocks: Collection[platform.Block], move: Direction, jump: bool = False, *args, **kwargs) -> None:
        if self._check_collision_from_predicate(lambda block: block.deadly, blocks) or self.rect.x < 0:
            self.state = State.FAILED

        if self._check_collision_from_predicate(lambda block: block.level_end, blocks):
            self.state = State.COMPLETED

        side_collisions = self._check_side_collision(blocks)
        if side_collisions == Direction.RIGHT:
            self.x_offset -= 1

        elif side_collisions == Direction.LEFT:
            self.x_offset += 1

        else:
            self.x_offset += self.dx

        if self._check_bottom_collision(blocks):
            if jump:
                self.dy = -self.jump_strength
            else:
                self.rect.y -= 1
                self.dy = 0

        else:
            self.dy += self.gravity

        if abs(self.dx) < self.move_speed:
            if move == Direction.LEFT:
                self.dx -= 1
            elif move == Direction.RIGHT:
                self.dx += 1
        if abs(self.dx > self.move_speed) or move == Direction.NONE:
            if self.dx > 0:
                self.dx -= 1

            elif self.dx < 0:
                self.dx += 1

        self.rect.y += self.dy

    def _check_side_collision(self, blocks: Collection[platform.Block]) -> Direction:
        for block in blocks:
            if block.solid and self.rect.colliderect(block.rect):
                    if self.rect.right >= block.rect.left > self.rect.centerx:
                        return Direction.RIGHT

                    elif self.rect.left <= block.rect.right < self.rect.centerx:
                        return Direction.LEFT

        return Direction.NONE

    def _check_bottom_collision(self, blocks: Collection[platform.Block]) -> bool:
        for block in blocks:
            if block.solid and self.rect.colliderect(block.rect):
                if block.rect.top <= self.rect.bottom:
                    return True
        return False

    def _check_collision_from_predicate(self, predicate: Callable[[platform.Block], bool],
                                        blocks: Collection[platform.Block]) -> bool:
        return any(self.rect.colliderect(block) for block in blocks if predicate(block))
