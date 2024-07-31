import pygame

from collections.abc import *

import json

import platform
import player
from constants import *


class Level:
    def __init__(self, player: player.Player, blocks: Collection[platform.Block]):
        self.player = pygame.sprite.GroupSingle(player)
        self.blocks = pygame.sprite.Group(blocks)

    @property
    def state(self):
        return self.player.sprite.state

    def update(self) -> None:
        if self.state == player.State.PLAYING:
            keys = pygame.key.get_pressed()

            player_move_direction = player.Direction.NONE
            if not (keys[pygame.K_a] and keys[pygame.K_d]):
                if keys[pygame.K_a]:
                    player_move_direction = player.Direction.LEFT

                elif keys[pygame.K_d]:
                    player_move_direction = player.Direction.RIGHT

            self.blocks.update(self.player.sprite.x_offset)
            self.player.update(self.blocks.sprites(), player_move_direction, keys[pygame.K_w])

    def draw(self, screen: pygame.Surface) -> None:
        if self.state == player.State.PLAYING:
            screen.fill(BACKGROUND_COLOR)
            self.blocks.draw(screen)
            self.player.draw(screen)

        elif self.state == player.State.FAILED:
            screen.blit(LEVEL_FAILED_TEXT,
                        ((screen.get_width() - LEVEL_FAILED_TEXT.get_width()) / 2,
                         (screen.get_height() - LEVEL_FAILED_TEXT.get_height()) / 2))

        elif self.state == player.State.COMPLETED:
            screen.blit(LEVEL_COMPLETED_TEXT,
                        ((screen.get_width() - LEVEL_COMPLETED_TEXT.get_width()) / 2,
                         (screen.get_height() - LEVEL_COMPLETED_TEXT.get_height()) / 2))


def parse_level(level_filepath: str) -> Level:
    with open(level_filepath, "r") as fp:
        level = json.load(fp)

    return Level(player.Player(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2, PLAYER_SIZE, PLAYER_COLOR, 8, 20, 1),
                 [_parse_block(block) for block in level])


def _parse_block(block: dict) -> platform.Block:
    return platform.Block(*block["bounds"], **block.get("attributes", {}))
