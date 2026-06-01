"""Main menu state for 2048."""

import math
import pygame

from src.states.base_state import BaseState
from src.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE,
    TILE_COLORS, BG_COLOR, TITLE_COLOR, BUTTON_COLOR,
    BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR,
)
from src.ui.button import Button


class MenuState(BaseState):
    """Main menu with title and navigation buttons."""

    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.Font(None, 120)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.button_font = pygame.font.Font(None, 36)
        self.time_elapsed = 0.0
        self.buttons: list[Button] = []
        self._create_buttons()

    def _create_buttons(self):
        """Create menu buttons centered on screen."""
        button_width = 240
        button_height = 50
        spacing = 16
        start_y = 320

        items = [
            ("Classic 2048", self._start_classic),
            ("Fibonacci Mode", self._start_fibonacci),
            ("Continue", lambda: self.game.change_state("play_continue")),
            ("Tutorial", lambda: self.game.change_state("tutorial")),
            ("Learn", lambda: self.game.change_state("learn")),
            ("Settings", lambda: self.game.change_state("settings")),
        ]

        for i, (text, callback) in enumerate(items):
            x = (WINDOW_WIDTH - button_width) // 2
            y = start_y + i * (button_height + spacing)
            rect = pygame.Rect(x, y, button_width, button_height)
            btn = Button(
                rect=rect,
                text=text,
                font=self.button_font,
                color=BUTTON_COLOR,
                hover_color=BUTTON_HOVER_COLOR,
                text_color=BUTTON_TEXT_COLOR,
                callback=callback,
            )
            self.buttons.append(btn)

    def _start_classic(self):
        """Start classic 2048 mode."""
        self.game.game_mode = "classic"
        self.game.change_state("play")

    def _start_fibonacci(self):
        """Start Fibonacci mode."""
        self.game.game_mode = "fibonacci"
        self.game.change_state("play")

    def enter(self):
        has_save = self.game.save_manager.has_save()
        self.buttons[2].visible = has_save
        self.buttons[2].enabled = has_save

    def handle_event(self, event: pygame.event.Event):
        for button in self.buttons:
            button.handle_event(event)

    def update(self, dt: float):
        self.time_elapsed += dt

    def render(self, surface: pygame.Surface):
        surface.fill(BG_COLOR)

        self._render_animated_background(surface)

        title_surf = self.title_font.render("2048", True, TITLE_COLOR)
        title_rect = title_surf.get_rect(centerx=WINDOW_WIDTH // 2, y=80)
        surface.blit(title_surf, title_rect)

        subtitle_surf = self.subtitle_font.render(
            "Join the tiles, get to 2048!", True, TITLE_COLOR
        )
        subtitle_rect = subtitle_surf.get_rect(centerx=WINDOW_WIDTH // 2, y=200)
        surface.blit(subtitle_surf, subtitle_rect)

        for button in self.buttons:
            button.render(surface)

    def _render_animated_background(self, surface: pygame.Surface):
        """Draw subtle color-shifting grid cells in the background."""
        cell_size = 60
        padding = 6
        cols = WINDOW_WIDTH // (cell_size + padding) + 1
        rows = WINDOW_HEIGHT // (cell_size + padding) + 1
        t = self.time_elapsed / 1000.0

        for row in range(rows):
            for col in range(cols):
                phase = (row + col) * 0.5 + t * 0.3
                alpha = int(15 + 10 * math.sin(phase))
                x = col * (cell_size + padding)
                y = row * (cell_size + padding)
                cell_surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                cell_surf.fill((205, 193, 180, alpha))
                surface.blit(cell_surf, (x, y))
