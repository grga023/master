"""Theme management system."""

from typing import Any


# Default themes
THEMES = {
    "classic": {
        "name": "Classic",
        "bg_color": (250, 248, 239),
        "grid_color": (187, 173, 160),
        "empty_cell_color": (205, 193, 180),
        "score_bg": (187, 173, 160),
        "score_text": (249, 246, 242),
        "title_color": (119, 110, 101),
        "button_color": (143, 122, 102),
        "button_hover": (165, 145, 125),
        "button_text": (249, 246, 242),
        "tile_colors": {
            0: (205, 193, 180), 2: (238, 228, 218), 4: (237, 224, 200),
            8: (242, 177, 121), 16: (245, 149, 99), 32: (246, 124, 95),
            64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 204, 97),
            512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 46),
        },
        "tile_text_dark": (119, 110, 101),
        "tile_text_light": (249, 246, 242),
    },
    "dark": {
        "name": "Dark",
        "bg_color": (30, 30, 40),
        "grid_color": (50, 50, 65),
        "empty_cell_color": (60, 60, 75),
        "score_bg": (50, 50, 65),
        "score_text": (220, 220, 230),
        "title_color": (220, 220, 230),
        "button_color": (70, 70, 90),
        "button_hover": (90, 90, 110),
        "button_text": (220, 220, 230),
        "tile_colors": {
            0: (60, 60, 75), 2: (80, 80, 100), 4: (90, 90, 120),
            8: (180, 120, 60), 16: (200, 100, 50), 32: (210, 80, 60),
            64: (220, 60, 40), 128: (200, 170, 50), 256: (200, 165, 40),
            512: (200, 160, 30), 1024: (200, 155, 20), 2048: (200, 150, 10),
        },
        "tile_text_dark": (200, 200, 210),
        "tile_text_light": (240, 240, 245),
    },
    "ocean": {
        "name": "Ocean",
        "bg_color": (230, 240, 250),
        "grid_color": (100, 150, 200),
        "empty_cell_color": (170, 200, 230),
        "score_bg": (100, 150, 200),
        "score_text": (255, 255, 255),
        "title_color": (40, 80, 120),
        "button_color": (60, 120, 180),
        "button_hover": (80, 140, 200),
        "button_text": (255, 255, 255),
        "tile_colors": {
            0: (170, 200, 230), 2: (180, 210, 240), 4: (150, 195, 235),
            8: (100, 170, 220), 16: (70, 150, 210), 32: (50, 130, 200),
            64: (30, 110, 190), 128: (20, 100, 180), 256: (15, 90, 170),
            512: (10, 80, 160), 1024: (5, 70, 150), 2048: (0, 60, 140),
        },
        "tile_text_dark": (40, 80, 120),
        "tile_text_light": (255, 255, 255),
    },
}


class ThemeManager:
    """Manages color themes for the game."""

    def __init__(self):
        self.themes = THEMES.copy()
        self.current_theme_name = "classic"

    @property
    def current_theme(self) -> dict[str, Any]:
        """Get the current theme dictionary."""
        return self.themes[self.current_theme_name]

    def switch_theme(self, name: str) -> bool:
        """Switch to a named theme. Returns True if successful."""
        if name in self.themes:
            self.current_theme_name = name
            return True
        return False

    def get_color(self, key: str) -> tuple:
        """Get a color value from the current theme."""
        return self.current_theme.get(key, (255, 0, 255))  # Magenta for missing

    def get_tile_color(self, value: int) -> tuple[int, int, int]:
        """Get the background color for a tile value."""
        tile_colors = self.current_theme["tile_colors"]
        if value in tile_colors:
            return tile_colors[value]
        # For values > 2048, use the 2048 color
        return tile_colors.get(2048, (237, 194, 46))

    def get_tile_text_color(self, value: int) -> tuple[int, int, int]:
        """Get the text color for a tile value."""
        if value <= 4:
            return self.current_theme["tile_text_dark"]
        return self.current_theme["tile_text_light"]

    def get_theme_names(self) -> list[str]:
        """Get list of available theme names."""
        return list(self.themes.keys())

    def next_theme(self) -> str:
        """Switch to the next theme in rotation."""
        names = self.get_theme_names()
        idx = names.index(self.current_theme_name)
        next_idx = (idx + 1) % len(names)
        self.current_theme_name = names[next_idx]
        return self.current_theme_name

    def to_dict(self) -> dict[str, str]:
        """Export theme settings."""
        return {"current_theme": self.current_theme_name}

    def load_from_dict(self, data: dict[str, str]):
        """Load theme settings."""
        name = data.get("current_theme", "classic")
        self.switch_theme(name)
