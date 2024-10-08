import json
from collections.abc import *

import pygame

import platform
import player
from constants import *


class Level:
    def __init__(self, player: player.Player, blocks: Collection[platform.Block]):
        self._player = pygame.sprite.GroupSingle(player)
        self._blocks = pygame.sprite.Group(blocks)

    @property
    def state(self):
        return self._player.sprite.state

    def update(self) -> None:
        if self.state == player.State.PLAYING:
            keys = pygame.key.get_pressed()

            player_move_direction = None
            if not (keys[KEYMAP.left] and keys[KEYMAP.right]):
                if keys[KEYMAP.left]:
                    player_move_direction = player.Direction.LEFT

                elif keys[KEYMAP.right]:
                    player_move_direction = player.Direction.RIGHT

            self._blocks.update(self._player.sprite.x_offset)
            self._player.update(self._blocks.sprites(), player_move_direction, keys[KEYMAP.jump])

    def draw(self, screen: pygame.Surface) -> None:
        if self.state == player.State.PLAYING:
            screen.fill(BACKGROUND_COLOR)
            self._blocks.draw(screen)
            self._player.draw(screen)

        elif self.state == player.State.FAILED:
            screen.blit(LEVEL_FAILED_TEXT,
                        ((screen.get_width() - LEVEL_FAILED_TEXT.get_width()) / 2,
                         (screen.get_height() - LEVEL_FAILED_TEXT.get_height()) / 2))

        elif self.state == player.State.COMPLETED:
            screen.blit(LEVEL_COMPLETED_TEXT,
                        ((screen.get_width() - LEVEL_COMPLETED_TEXT.get_width()) / 2,
                         (screen.get_height() - LEVEL_COMPLETED_TEXT.get_height()) / 2))


def parse_level(level_filepath: str) -> Level:
    """
    Parse a json file representing a level.
    :param level_filepath: The path of the json file representing the level.
    :return: A corresponding level.
    """
    return Level(player.Player(**DEFAULT_PLAYER_ARGS), parse_blocks(level_filepath))


def parse_blocks(level_filepath: str) -> Collection[platform.Block]:
    """
    Parse a json file representing a level.
    :param level_filepath: The path of the json file representing the level.
    :return: The corresponding blocks for the level.
    """

    with open(level_filepath, "r") as fp:
        level = json.load(fp)

    return [_parse_block(block) for block in level]


def _parse_block(block: dict) -> platform.Block:
    match block.get("type"):
        case "moving":
            BlockType = platform.MovingBlock
        case _:
            BlockType = platform.Block

    return BlockType(*block["bounds"], **block.get("attributes", {}))
