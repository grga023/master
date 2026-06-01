"""Victory overlay state for reaching 2048."""

import math
import pygame

from src.states.base_state import BaseState
from src.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR,
)
from src.ui.button import Button


class VictoryState(BaseState):
    """Celebratory overlay when the player reaches 2048."""

    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.Font(None, 80)
        self.subtitle_font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 36)
        self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((237, 194, 46, 180))
        self.time_elapsed = 0.0
        self.buttons = self._create_buttons()

    def _create_buttons(self) -> list[Button]:
        button_width = 200
        button_height = 50
        spacing = 20
        start_y = WINDOW_HEIGHT // 2 + 30

        items = [
            ("Keep Playing", lambda: self.game.pop_state()),
            ("New Game", lambda: self.game.change_state("play")),
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

    def enter(self):
        self.game.audio_manager.play_sfx("victory")

    def handle_event(self, event: pygame.event.Event):
        for button in self.buttons:
            button.handle_event(event)

    def update(self, dt: float):
        self.time_elapsed += dt

    def render(self, surface: pygame.Surface):
        surface.blit(self.overlay, (0, 0))

        # Pulsing title
        t = self.time_elapsed / 1000.0
        scale = 1.0 + 0.05 * math.sin(t * 3.0)
        base_size = 80
        font = pygame.font.Font(None, int(base_size * scale))

        title_surf = font.render("You Win!", True, (255, 255, 255))
        title_rect = title_surf.get_rect(centerx=WINDOW_WIDTH // 2, centery=WINDOW_HEIGHT // 2 - 80)
        surface.blit(title_surf, title_rect)

        subtitle_surf = self.subtitle_font.render(
            "You reached 2048!", True, (255, 255, 255)
        )
        subtitle_rect = subtitle_surf.get_rect(centerx=WINDOW_WIDTH // 2, y=WINDOW_HEIGHT // 2 - 20)
        surface.blit(subtitle_surf, subtitle_rect)

        for button in self.buttons:
            button.render(surface)
