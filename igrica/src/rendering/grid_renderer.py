"""Grid background rendering."""

import pygame
from src.constants import (
    GRID_SIZE, CELL_SIZE, CELL_PADDING, GRID_OFFSET_X, GRID_OFFSET_Y,
    GRID_COLOR, EMPTY_CELL_COLOR,
)


class GridRenderer:
    """Renders the game grid background."""

    def __init__(self, theme_manager=None):
        self.theme_manager = theme_manager
        self._grid_rect = pygame.Rect(
            GRID_OFFSET_X - CELL_PADDING,
            GRID_OFFSET_Y - CELL_PADDING,
            GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * CELL_PADDING,
            GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * CELL_PADDING,
        )

    def get_grid_color(self) -> tuple:
        if self.theme_manager:
            return self.theme_manager.get_color("grid_color")
        return GRID_COLOR

    def get_empty_color(self) -> tuple:
        if self.theme_manager:
            return self.theme_manager.get_color("empty_cell_color")
        return EMPTY_CELL_COLOR

    def cell_to_pixel(self, row: int, col: int) -> tuple[int, int]:
        """Convert grid cell position to pixel position (top-left of cell)."""
        x = GRID_OFFSET_X + col * (CELL_SIZE + CELL_PADDING)
        y = GRID_OFFSET_Y + row * (CELL_SIZE + CELL_PADDING)
        return x, y

    def render(self, surface: pygame.Surface):
        """Render the grid background and empty cells."""
        pygame.draw.rect(
            surface, self.get_grid_color(), self._grid_rect, border_radius=8
        )

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x, y = self.cell_to_pixel(row, col)
                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(
                    surface, self.get_empty_color(), cell_rect, border_radius=6
                )
