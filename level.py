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
        self.is_running = True

    def update(self):
        if self.is_running:
            keys = pygame.key.get_pressed()

            self.blocks.update()
            self.player.update(self.blocks.sprites(), keys[pygame.K_SPACE])

            if self.player.sprite.is_dead:
                self.is_running = False

    def draw(self, screen):
        if self.is_running:
            screen.fill(BACKGROUND_COLOR)
            self.blocks.draw(screen)
            self.player.draw(screen)
