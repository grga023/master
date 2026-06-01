"""Toast notification widget."""

import pygame
from typing import Optional


class Toast:
    """Temporary notification that appears and fades out."""

    def __init__(
        self,
        text: str,
        font: pygame.font.Font,
        duration_ms: float = 3000.0,
        position: str = "bottom",  # "top", "center", "bottom"
        color: tuple[int, int, int] = (119, 110, 101),
        bg_color: tuple[int, int, int] = (238, 228, 218),
        padding: int = 16,
    ):
        self.text = text
        self.font = font
        self.duration_ms = duration_ms
        self.position = position
        self.color = color
        self.bg_color = bg_color
        self.padding = padding
        self.elapsed_ms = 0.0
        self.alive = True
        self._fade_duration = 500.0  # ms for fade in/out

    @property
    def progress(self) -> float:
        return min(1.0, self.elapsed_ms / self.duration_ms)

    @property
    def alpha(self) -> int:
        """Calculate current alpha based on fade in/out."""
        if self.elapsed_ms < self._fade_duration:
            # Fade in
            return int(255 * (self.elapsed_ms / self._fade_duration))
        elif self.elapsed_ms > self.duration_ms - self._fade_duration:
            # Fade out
            remaining = self.duration_ms - self.elapsed_ms
            return int(255 * max(0, remaining / self._fade_duration))
        return 255

    def update(self, dt_ms: float):
        """Update toast timer."""
        if not self.alive:
            return
        self.elapsed_ms += dt_ms
        if self.elapsed_ms >= self.duration_ms:
            self.alive = False

    def render(self, surface: pygame.Surface, screen_width: int, screen_height: int):
        """Render the toast notification."""
        if not self.alive:
            return

        alpha = self.alpha
        if alpha <= 0:
            return

        text_surf = self.font.render(self.text, True, self.color)
        width = text_surf.get_width() + self.padding * 2
        height = text_surf.get_height() + self.padding * 2

        # Position
        x = (screen_width - width) // 2
        if self.position == "top":
            y = 20
        elif self.position == "center":
            y = (screen_height - height) // 2
        else:  # bottom
            y = screen_height - height - 60

        # Draw background with alpha
        toast_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        bg_with_alpha = (*self.bg_color, alpha)
        pygame.draw.rect(
            toast_surf, bg_with_alpha, pygame.Rect(0, 0, width, height),
            border_radius=8
        )

        # Draw text with alpha
        text_with_alpha = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
        text_with_alpha.blit(text_surf, (0, 0))
        text_with_alpha.set_alpha(alpha)
        toast_surf.blit(text_with_alpha, (self.padding, self.padding))

        surface.blit(toast_surf, (x, y))


class ToastManager:
    """Manages multiple toast notifications."""

    def __init__(self, max_toasts: int = 3):
        self.toasts: list[Toast] = []
        self.max_toasts = max_toasts

    def show(self, text: str, font: pygame.font.Font, duration_ms: float = 3000.0,
             position: str = "bottom", **kwargs):
        """Show a new toast notification."""
        toast = Toast(text, font, duration_ms, position, **kwargs)
        self.toasts.append(toast)
        if len(self.toasts) > self.max_toasts:
            self.toasts.pop(0)

    def update(self, dt_ms: float):
        """Update all toasts."""
        for toast in self.toasts:
            toast.update(dt_ms)
        self.toasts = [t for t in self.toasts if t.alive]

    def render(self, surface: pygame.Surface, screen_width: int, screen_height: int):
        """Render all active toasts."""
        for toast in self.toasts:
            toast.render(surface, screen_width, screen_height)

    def clear(self):
        """Remove all toasts."""
        self.toasts.clear()
