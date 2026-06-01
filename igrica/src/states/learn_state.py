"""Educational 'Learn' state with math and strategy content."""

import pygame

from src.states.base_state import BaseState
from src.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, TITLE_COLOR,
    BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR,
)
from src.ui.button import Button
from src.educational.math_overlay import MathOverlay


TAB_CONTENT = {
    "Powers of 2": [
        "2\u00b9 = 2      2\u00b2 = 4      2\u00b3 = 8",
        "2\u2074 = 16    2\u2075 = 32    2\u2076 = 64",
        "2\u2077 = 128   2\u2078 = 256   2\u2079 = 512",
        "2\u00b9\u2070 = 1024   2\u00b9\u00b9 = 2048",
        "",
        "Each merge doubles the tile value.",
        "Reaching 2048 requires 11 merges from 2.",
    ],
    "Probabilities": [
        "New tiles: 90% chance of 2, 10% chance of 4.",
        "",
        "With 16 cells and random spawns,",
        "board space is your most valuable resource.",
        "",
        "Average moves to fill a 4x4 board: ~40",
        "Keep empty cells available for flexibility.",
    ],
    "Strategy": [
        "1. Pick a corner and keep your max tile there.",
        "2. Build a decreasing chain along one edge.",
        "3. Never push your max tile away from its corner.",
        "4. Keep the row/column of your max tile full.",
        "5. Plan 2-3 moves ahead before acting.",
        "",
        "Advanced: Use the snake pattern for high scores.",
    ],
}

TAB_NAMES = list(TAB_CONTENT.keys())


class LearnState(BaseState):
    """Educational content about powers of 2, probabilities, and strategy."""

    def __init__(self, game):
        super().__init__(game)
        self.current_tab = 0
        self.title_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 26)
        self.button_font = pygame.font.Font(None, 30)
        self.tab_font = pygame.font.Font(None, 28)
        self.buttons = self._create_buttons()
        self.tab_buttons = self._create_tab_buttons()

    def _create_buttons(self) -> list[Button]:
        back_btn = Button(
            rect=pygame.Rect(20, WINDOW_HEIGHT - 70, 100, 45),
            text="Back",
            font=self.button_font,
            color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text_color=BUTTON_TEXT_COLOR,
            callback=lambda: self.game.change_state("menu"),
        )
        return [back_btn]

    def _create_tab_buttons(self) -> list[Button]:
        tab_width = 160
        spacing = 15
        total_width = len(TAB_NAMES) * tab_width + (len(TAB_NAMES) - 1) * spacing
        start_x = (WINDOW_WIDTH - total_width) // 2
        y = 80

        tabs = []
        for i, name in enumerate(TAB_NAMES):
            x = start_x + i * (tab_width + spacing)
            rect = pygame.Rect(x, y, tab_width, 40)
            btn = Button(
                rect=rect, text=name, font=self.tab_font,
                color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR,
                text_color=BUTTON_TEXT_COLOR,
                callback=lambda idx=i: self._select_tab(idx),
            )
            tabs.append(btn)
        return tabs

    def _select_tab(self, index: int):
        self.current_tab = index

    def enter(self):
        self.current_tab = 0

    def handle_event(self, event: pygame.event.Event):
        for button in self.buttons:
            button.handle_event(event)
        for tab in self.tab_buttons:
            tab.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_state("menu")

    def update(self, dt: float):
        pass

    def render(self, surface: pygame.Surface):
        surface.fill(BG_COLOR)

        # Title
        title_surf = self.title_font.render("Learn", True, TITLE_COLOR)
        title_rect = title_surf.get_rect(centerx=WINDOW_WIDTH // 2, y=25)
        surface.blit(title_surf, title_rect)

        # Tab buttons (highlight active)
        for i, tab in enumerate(self.tab_buttons):
            if i == self.current_tab:
                tab.color = BUTTON_HOVER_COLOR
            else:
                tab.color = BUTTON_COLOR
            tab.render(surface)

        # Content
        tab_name = TAB_NAMES[self.current_tab]
        lines = TAB_CONTENT[tab_name]
        y = 160
        for line in lines:
            if line:
                line_surf = self.text_font.render(line, True, TITLE_COLOR)
                line_rect = line_surf.get_rect(centerx=WINDOW_WIDTH // 2, y=y)
                surface.blit(line_surf, line_rect)
            y += 36

        for button in self.buttons:
            button.render(surface)
