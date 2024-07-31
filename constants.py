from pygame import font
font.init()

WINDOW_SIZE = (1280, 720)
BACKGROUND_COLOR = "cyan"

DEFAULT_BLOCK_COLOR = "darkgray"

PLAYER_SIZE = 50
PLAYER_COLOR = "red"

LEVEL_FONT = font.SysFont("Serif", 60)
LEVEL_COMPLETED_TEXT = LEVEL_FONT.render("Level Completed!", True, "darkgreen")
LEVEL_FAILED_TEXT = LEVEL_FONT.render("Level Failed.", True, "red")

BUTTON_SIZE = (300, 150)
BUTTON_LEFT_SPACING = (WINDOW_SIZE[0] - BUTTON_SIZE[0]) // 2
BUTTON_FONT = font.SysFont("Serif", 25)
BUTTON_COLOR = "gray"
