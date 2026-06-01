"""Tile drawing with rounded rectangles and text."""

import pygame
from src.constants import (
    CELL_SIZE, FONT_SIZES, TILE_COLORS, TILE_TEXT_COLORS, DEFAULT_TILE_TEXT_COLOR,
)


class TileRenderer:
    """Renders individual tiles with values and colors."""

    def __init__(self, theme_manager=None):
        self.theme_manager = theme_manager
        self._fonts: dict[int, pygame.font.Font] = {}
        self._init_fonts()
        self.color_override = None

    def _init_fonts(self):
        """Initialize fonts for different digit counts."""
        for digits, size in FONT_SIZES.items():
            self._fonts[digits] = pygame.font.Font(None, size)

    def _get_font(self, value: int) -> pygame.font.Font:
        """Get appropriate font size for tile value."""
        digits = len(str(value))
        return self._fonts.get(digits, self._fonts.get(5, self._fonts[1]))

    def get_tile_color(self, value: int) -> tuple[int, int, int]:
        """Get background color for a tile value."""
        if self.color_override:
            return self.color_override.get(value, self.color_override.get(0, (205, 193, 180)))
        if self.theme_manager:
            return self.theme_manager.get_tile_color(value)
        return TILE_COLORS.get(value, TILE_COLORS.get(2048, (237, 194, 46)))

    def get_text_color(self, value: int) -> tuple[int, int, int]:
        """Get text color for a tile value."""
        if self.color_override:
            from src.constants import FIBONACCI_TILE_TEXT_COLORS
            return FIBONACCI_TILE_TEXT_COLORS.get(value, DEFAULT_TILE_TEXT_COLOR)
        if self.theme_manager:
            return self.theme_manager.get_tile_text_color(value)
        return TILE_TEXT_COLORS.get(value, DEFAULT_TILE_TEXT_COLOR)

    def render_tile(self, surface: pygame.Surface, x: int, y: int, value: int,
                    scale: float = 1.0, alpha: int = 255):
        """Render a single tile at the given position."""
        if value == 0:
            return

        size = int(CELL_SIZE * scale)
        offset = (CELL_SIZE - size) // 2
        tile_rect = pygame.Rect(x + offset, y + offset, size, size)

        if alpha < 255:
            tile_surf = pygame.Surface((size, size), pygame.SRCALPHA)
            color = (*self.get_tile_color(value), alpha)
            pygame.draw.rect(tile_surf, color, pygame.Rect(0, 0, size, size), border_radius=6)
            font = self._get_font(value)
            text_color = (*self.get_text_color(value), alpha)
            text_surf = font.render(str(value), True, text_color)
            text_rect = text_surf.get_rect(center=(size // 2, size // 2))
            tile_surf.blit(text_surf, text_rect)
            surface.blit(tile_surf, (x + offset, y + offset))
        else:
            bg_color = self.get_tile_color(value)
            pygame.draw.rect(surface, bg_color, tile_rect, border_radius=6)
            font = self._get_font(value)
            text_color = self.get_text_color(value)
            text_surf = font.render(str(value), True, text_color)
            text_rect = text_surf.get_rect(center=tile_rect.center)
            surface.blit(text_surf, text_rect)
