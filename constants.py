from pygame import font
from pygame import K_a, K_d, K_w, K_SPACE
from keymap import KeyMap

font.init()

WINDOW_SIZE = (1280, 720)
BACKGROUND_COLOR = "cyan"

DEFAULT_BLOCK_COLOR = "darkgray"

DEFAULT_PLAYER_ARGS = {
    "x": WINDOW_SIZE[0] / 2,
    "y": WINDOW_SIZE[1] / 2,
    "size": 50,
    "color": "red",
    "move_speed": 8,
    "jump_strength": 20,
    "acceleration": 1,
    "gravity": 1
}

PLAYER_DISLODGE_STRENGTH = 2

LEVEL_FONT = font.SysFont("Serif", 60)
LEVEL_COMPLETED_TEXT = LEVEL_FONT.render("Level Completed!", True, "darkgreen")
LEVEL_FAILED_TEXT = LEVEL_FONT.render("Level Failed.", True, "red")

BUTTON_SIZE = (200, 100)
BUTTON_SIDE_SPACING = (WINDOW_SIZE[0] - BUTTON_SIZE[0]) // 4
BUTTON_FONT = font.SysFont("Serif", 25)
BUTTON_COLOR = "gray"

KEYMAP = KeyMap(
    left=K_a,
    right=K_d,
    jump=K_w,
    skip=K_SPACE
)
