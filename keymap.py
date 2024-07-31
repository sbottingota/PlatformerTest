import pygame

KeyType = type(pygame.K_a)


class KeyMap:
    def __init__(self, *, left: KeyType, right: KeyType, jump: KeyType, skip: KeyType):
        self.left = left
        self.right = right
        self.jump = jump
        self.skip = skip
