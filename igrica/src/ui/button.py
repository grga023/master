"""Clickable button widget."""

import pygame
from typing import Callable, Optional


class Button:
    """A clickable button with hover effects."""

    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int] = (143, 122, 102),
        hover_color: tuple[int, int, int] = (165, 145, 125),
        text_color: tuple[int, int, int] = (249, 246, 242),
        callback: Optional[Callable] = None,
        border_radius: int = 6,
    ):
        self.rect = rect
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.callback = callback
        self.border_radius = border_radius
        self.hovered = False
        self.pressed = False
        self.visible = True
        self.enabled = True

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events. Returns True if button was clicked."""
        if not self.visible or not self.enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed and self.rect.collidepoint(event.pos):
                self.pressed = False
                if self.callback:
                    self.callback()
                return True
            self.pressed = False

        return False

    def render(self, surface: pygame.Surface):
        """Draw the button."""
        if not self.visible:
            return

        color = self.hover_color if self.hovered else self.color
        if not self.enabled:
            color = tuple(min(255, c + 60) for c in self.color)

        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
