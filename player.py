import pygame
from constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, jump_strength, gravity, *groups):
        super().__init__(*groups)

        self.image = pygame.Surface((size, size))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.jump_strength = jump_strength
        self.gravity = gravity

        self.dy = 0

    def update(self, blocks, jump=False, *args, **kwargs):
        if self._check_side_collision(blocks):
            self.rect.x -= 3

        if self._check_bottom_collision(blocks):
            if jump:
                self.dy = -self.jump_strength
            else:
                self.rect.y -= BLOCK_MOVE_AMOUNT + 1
                self.dy = 0

        else:
            self.dy += self.gravity

        self.rect.y += self.dy

    def _check_side_collision(self, blocks):
        for block in blocks:
            if self.rect.colliderect(block.rect):
                return self.rect.right >= block.rect.left > self.rect.centerx

        return False

    def _check_bottom_collision(self, blocks):
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if block.rect.top <= self.rect.bottom:
                    return True
        return False
