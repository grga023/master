"""Panel/container widget."""

import pygame
from typing import Optional


class Panel:
    """A rectangular panel that serves as a background container."""

    def __init__(
        self,
        rect: pygame.Rect,
        color: tuple[int, int, int, ...] = (187, 173, 160),
        border_radius: int = 6,
        border_color: Optional[tuple[int, int, int]] = None,
        border_width: int = 0,
        alpha: int = 255,
    ):
        self.rect = rect
        self.color = color
        self.border_radius = border_radius
        self.border_color = border_color
        self.border_width = border_width
        self.alpha = alpha
        self.visible = True

    def render(self, surface: pygame.Surface):
        """Draw the panel."""
        if not self.visible:
            return

        if self.alpha < 255:
            panel_surf = pygame.Surface(
                (self.rect.width, self.rect.height), pygame.SRCALPHA
            )
            color_with_alpha = (*self.color[:3], self.alpha)
            pygame.draw.rect(
                panel_surf,
                color_with_alpha,
                pygame.Rect(0, 0, self.rect.width, self.rect.height),
                border_radius=self.border_radius,
            )
            surface.blit(panel_surf, self.rect.topleft)
        else:
            pygame.draw.rect(
                surface, self.color, self.rect, border_radius=self.border_radius
            )

        if self.border_color and self.border_width > 0:
            pygame.draw.rect(
                surface,
                self.border_color,
                self.rect,
                width=self.border_width,
                border_radius=self.border_radius,
            )
