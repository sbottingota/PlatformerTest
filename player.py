from collections.abc import *

import enum

import pygame

import platform
from constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, size: int, color: str, jump_strength: int, gravity: int,
                 *groups: pygame.sprite.Group):
        super().__init__(*groups)

        self.image = pygame.Surface((size, size))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.jump_strength = jump_strength
        self.gravity = gravity

        self.state = State.PLAYING

        self.dy = 0

    def update(self, blocks: Collection[platform.Block], jump: bool = False, *args, **kwargs) -> None:
        if self._check_collision_from_predicate(lambda block: block.deadly, blocks) or self.rect.x < 0:
            self.state = State.FAILED

        if self._check_collision_from_predicate(lambda block: block.level_endblocks):
            self.state = State.COMPLETED

        if self._check_side_collision(blocks):
            self.rect.x -= BLOCK_MOVE_AMOUNT + 1

        if self._check_bottom_collision(blocks):
            if jump:
                self.dy = -self.jump_strength
            else:
                self.rect.y -= 1
                self.dy = 0

        else:
            self.dy += self.gravity

        self.rect.y += self.dy

    def _check_side_collision(self, blocks: Collection[platform.Block]) -> bool:
        for block in blocks:
            if block.solid and self.rect.colliderect(block.rect):
                return self.rect.right >= block.rect.left > self.rect.centerx

        return False

    def _check_bottom_collision(self, blocks: Collection[platform.Block]) -> bool:
        for block in blocks:
            if block.solid and self.rect.colliderect(block.rect):
                if block.rect.top <= self.rect.bottom:
                    return True
        return False

    def _check_collision_from_predicate(self, condition: Callable[platform.Block, bool], blocks: Collection[platform.Block]) -> bool:
        return any(self.rect.colliderect(block) for block in blocks if condition(block))


class State(enum.Enum):
    PLAYING = 0
    FAILED = 1
    COMPLETED = 2
