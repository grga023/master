"""Settings state for theme, sound, and options."""

import pygame

from src.states.base_state import BaseState
from src.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, TITLE_COLOR,
    BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR,
)
from src.ui.button import Button


class SettingsState(BaseState):
    """Settings screen: theme, sound toggle, board size."""

    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.Font(None, 48)
        self.label_font = pygame.font.Font(None, 32)
        self.button_font = pygame.font.Font(None, 30)
        self.buttons = self._create_buttons()

    def _create_buttons(self) -> list[Button]:
        btn_width = 200
        btn_height = 45
        center_x = (WINDOW_WIDTH - btn_width) // 2
        start_y = 160
        spacing = 80

        theme_btn = Button(
            rect=pygame.Rect(center_x, start_y, btn_width, btn_height),
            text="Next Theme",
            font=self.button_font,
            color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text_color=BUTTON_TEXT_COLOR,
            callback=self._cycle_theme,
        )
        sound_btn = Button(
            rect=pygame.Rect(center_x, start_y + spacing, btn_width, btn_height),
            text="Sound: ON",
            font=self.button_font,
            color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text_color=BUTTON_TEXT_COLOR,
            callback=self._toggle_sound,
        )
        board_btn = Button(
            rect=pygame.Rect(center_x, start_y + spacing * 2, btn_width, btn_height),
            text="Board: 4x4",
            font=self.button_font,
            color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text_color=BUTTON_TEXT_COLOR,
            callback=None,
        )
        board_btn.enabled = False

        back_btn = Button(
            rect=pygame.Rect(center_x, WINDOW_HEIGHT - 90, btn_width, btn_height),
            text="Back",
            font=self.button_font,
            color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text_color=BUTTON_TEXT_COLOR,
            callback=lambda: self.game.change_state("menu"),
        )

        return [theme_btn, sound_btn, board_btn, back_btn]

    def enter(self):
        self._update_labels()

    def _cycle_theme(self):
        self.game.theme_manager.next_theme()
        self._update_labels()

    def _toggle_sound(self):
        self.game.audio_manager.toggle_mute()
        self._update_labels()

    def _update_labels(self):
        """Refresh button text to reflect current settings."""
        theme_name = self.game.theme_manager.current_theme_name
        self.buttons[0].text = f"Theme: {theme_name}"

        sound_on = not self.game.audio_manager.muted
        self.buttons[1].text = f"Sound: {'ON' if sound_on else 'OFF'}"

    def handle_event(self, event: pygame.event.Event):
        for button in self.buttons:
            button.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_state("menu")

    def update(self, dt: float):
        pass

    def render(self, surface: pygame.Surface):
        surface.fill(BG_COLOR)

        title_surf = self.title_font.render("Settings", True, TITLE_COLOR)
        title_rect = title_surf.get_rect(centerx=WINDOW_WIDTH // 2, y=40)
        surface.blit(title_surf, title_rect)

        # Section labels
        labels = ["Theme", "Sound", "Board Size (coming soon)"]
        start_y = 135
        spacing = 80
        for i, label in enumerate(labels):
            label_surf = self.label_font.render(label, True, TITLE_COLOR)
            label_rect = label_surf.get_rect(centerx=WINDOW_WIDTH // 2, y=start_y + i * spacing)
            surface.blit(label_surf, label_rect)

        for button in self.buttons:
            button.render(surface)
