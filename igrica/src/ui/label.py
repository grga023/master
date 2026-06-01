"""Text label widget."""

import pygame
from typing import Optional


class Label:
    """Simple text rendering widget."""

    def __init__(
        self,
        text: str,
        pos: tuple[int, int],
        font: pygame.font.Font,
        color: tuple[int, int, int] = (119, 110, 101),
        align: str = "topleft",
        antialias: bool = True,
    ):
        self.text = text
        self.pos = pos
        self.font = font
        self.color = color
        self.align = align
        self.antialias = antialias
        self.visible = True
        self._surface: Optional[pygame.Surface] = None
        self._dirty = True

    def set_text(self, text: str):
        """Update the label text."""
        if text != self.text:
            self.text = text
            self._dirty = True

    def set_color(self, color: tuple[int, int, int]):
        """Update the label color."""
        if color != self.color:
            self.color = color
            self._dirty = True

    def _render_surface(self):
        """Pre-render the text surface."""
        self._surface = self.font.render(self.text, self.antialias, self.color)
        self._dirty = False

    def render(self, surface: pygame.Surface):
        """Draw the label."""
        if not self.visible:
            return

        if self._dirty or self._surface is None:
            self._render_surface()

        rect = self._surface.get_rect()
        setattr(rect, self.align, self.pos)
        surface.blit(self._surface, rect)

    @property
    def width(self) -> int:
        if self._dirty or self._surface is None:
            self._render_surface()
        return self._surface.get_width()

    @property
    def height(self) -> int:
        if self._dirty or self._surface is None:
            self._render_surface()
        return self._surface.get_height()
