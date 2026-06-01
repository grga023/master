"""Pause overlay state."""

import pygame

from src.states.base_state import BaseState
from src.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR,
)
from src.ui.button import Button


class PauseState(BaseState):
    """Semi-transparent pause overlay with resume/restart/menu options."""

    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.Font(None, 72)
        self.button_font = pygame.font.Font(None, 36)
        self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 160))
        self.buttons = self._create_buttons()

    def _create_buttons(self) -> list[Button]:
        button_width = 200
        button_height = 50
        spacing = 20
        start_y = WINDOW_HEIGHT // 2 - 20

        items = [
            ("Resume", lambda: self.game.pop_state()),
            ("Restart", lambda: self.game.change_state("play")),
            ("Main Menu", lambda: self.game.change_state("menu")),
        ]

        buttons = []
        for i, (text, callback) in enumerate(items):
            x = (WINDOW_WIDTH - button_width) // 2
            y = start_y + i * (button_height + spacing)
            rect = pygame.Rect(x, y, button_width, button_height)
            buttons.append(Button(
                rect=rect, text=text, font=self.button_font,
                color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR,
                text_color=BUTTON_TEXT_COLOR, callback=callback,
            ))
        return buttons

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_p, pygame.K_ESCAPE):
                self.game.pop_state()
                return

        for button in self.buttons:
            button.handle_event(event)

    def update(self, dt: float):
        pass

    def render(self, surface: pygame.Surface):
        surface.blit(self.overlay, (0, 0))

        title_surf = self.title_font.render("PAUSED", True, (255, 255, 255))
        title_rect = title_surf.get_rect(centerx=WINDOW_WIDTH // 2, y=WINDOW_HEIGHT // 2 - 120)
        surface.blit(title_surf, title_rect)

        for button in self.buttons:
            button.render(surface)
