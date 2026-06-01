"""Game constants for 2048."""

# Window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 750
FPS = 60

# Grid
GRID_SIZE = 4
CELL_SIZE = 120
CELL_PADDING = 12
GRID_OFFSET_X = 30
GRID_OFFSET_Y = 180

# Animation timing (milliseconds)
ANIMATION_SLIDE_DURATION = 150
ANIMATION_MERGE_DURATION = 100
ANIMATION_SPAWN_DURATION = 150
PARTICLE_COUNT = 12
PARTICLE_LIFETIME = 400

# Font sizes by digit count
FONT_SIZES = {1: 55, 2: 50, 3: 40, 4: 32, 5: 28}

# Tile colors by value
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Text colors (dark for light tiles, white for the rest)
TILE_TEXT_COLORS = {
    2: (119, 110, 101),
    4: (119, 110, 101),
}
DEFAULT_TILE_TEXT_COLOR = (249, 246, 242)

# Background colors
BG_COLOR = (187, 173, 160)
GRID_COLOR = (187, 173, 160)
EMPTY_CELL_COLOR = (205, 193, 180)

# UI colors
SCORE_BG_COLOR = (187, 173, 160)
SCORE_TEXT_COLOR = (249, 246, 242)
SCORE_LABEL_COLOR = (238, 228, 218)
BUTTON_COLOR = (143, 122, 102)
BUTTON_HOVER_COLOR = (165, 145, 125)
BUTTON_TEXT_COLOR = (249, 246, 242)
TITLE_COLOR = (119, 110, 101)
SUBTITLE_COLOR = (119, 110, 101)

# Game modes
MODE_CLASSIC = "classic"
MODE_FIBONACCI = "fibonacci"

# Fibonacci settings
FIBONACCI_WIN_TARGET = 610

# Fibonacci tile colors (golden/amber palette)
FIBONACCI_TILE_COLORS = {
    0: (205, 193, 180),
    1: (255, 248, 225),
    2: (255, 236, 179),
    3: (255, 224, 130),
    5: (255, 213, 79),
    8: (255, 193, 7),
    13: (255, 160, 0),
    21: (245, 124, 0),
    34: (230, 81, 0),
    55: (191, 54, 12),
    89: (153, 0, 48),
    144: (106, 27, 154),
    233: (74, 20, 140),
    377: (49, 27, 146),
    610: (26, 35, 126),
    987: (13, 71, 161),
}

FIBONACCI_TILE_TEXT_COLORS = {
    1: (119, 110, 101),
    2: (119, 110, 101),
    3: (119, 110, 101),
    5: (119, 110, 101),
}
# All others use white: (249, 246, 242)

# Layout: game area vs progress tree panel
GAME_AREA_WIDTH = 600
TREE_PANEL_X = 610
TREE_PANEL_WIDTH = 180
