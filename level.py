import pygame

import json

import platform
import player
from constants import *


def parse_level(level_filepath):
    with open(level_filepath, "r") as fp:
        level = json.load(fp)

    return Level(player.Player(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2, PLAYER_SIZE, PLAYER_COLOR, 20, 1),
                 [_parse_block(block) for block in level])


def _parse_block(block):
    return platform.Block(*block["bounds"], **block.get("attributes", {}))


class Level:
    def __init__(self, player, blocks):
        self.player = pygame.sprite.GroupSingle(player)
        self.blocks = pygame.sprite.Group(blocks)

        self.get_state = lambda: player.state

    def update(self):
        if self.get_state() == player.State.PLAYING:
            keys = pygame.key.get_pressed()

            self.blocks.update()
            self.player.update(self.blocks.sprites(), keys[pygame.K_SPACE])

    def draw(self, screen: pygame.Surface):
        if self.get_state() == player.State.PLAYING:
            screen.fill(BACKGROUND_COLOR)
            self.blocks.draw(screen)
            self.player.draw(screen)

        elif self.get_state() == player.State.FAILED:
            screen.blit(LEVEL_FAILED_TEXT,
                        ((screen.get_width() - LEVEL_FAILED_TEXT.get_width()) / 2,
                         (screen.get_height() - LEVEL_FAILED_TEXT.get_height()) / 2))

        elif self.get_state() == player.State.COMPLETED:
            screen.blit(LEVEL_COMPLETED_TEXT,
                        ((screen.get_width() - LEVEL_COMPLETED_TEXT.get_width()) / 2,
                         (screen.get_height() - LEVEL_COMPLETED_TEXT.get_height()) / 2))

