"""Timeline bar widget for replay state."""
import pygame
from typing import Optional


class TimelineBar:
    """Horizontal timeline with progress and milestone markers."""

    def __init__(self, rect: pygame.Rect, total_steps: int,
                 milestones: list = None):
        self.rect = rect
        self.total_steps = max(total_steps, 1)
        self.current_step = 0
        self.milestones = milestones or []  # list of step indices
        
        self.bg_color = (187, 173, 160)
        self.fill_color = (143, 122, 102)
        self.milestone_color = (237, 194, 46)
        self.border_radius = 6

    def set_step(self, step: int):
        self.current_step = min(step, self.total_steps)

    def get_clicked_step(self, mouse_pos: tuple) -> Optional[int]:
        """If click is on the bar, return the step at that position."""
        if self.rect.collidepoint(mouse_pos):
            relative_x = mouse_pos[0] - self.rect.x
            fraction = relative_x / self.rect.width
            return int(fraction * self.total_steps)
        return None

    def render(self, surface: pygame.Surface):
        # Background
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=self.border_radius)
        
        # Filled portion
        if self.total_steps > 0:
            fill_width = int((self.current_step / self.total_steps) * self.rect.width)
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(surface, self.fill_color, fill_rect, border_radius=self.border_radius)
        
        # Milestone markers
        for step in self.milestones:
            x = self.rect.x + int((step / self.total_steps) * self.rect.width)
            pygame.draw.circle(surface, self.milestone_color, (x, self.rect.centery), 5)
