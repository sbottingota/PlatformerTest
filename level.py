import json

import platform


def parse_level(level_filepath):
    with open(level_filepath, "r") as fp:
        level = json.load(fp)

    return [_parse_block(block) for block in level]


def _parse_block(block):
    return platform.Block(*block["bounds"], **block.get("attributes", {}))
