"""Interactive tutorial state."""

import pygame

from src.states.base_state import BaseState
from src.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, TITLE_COLOR,
    BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR,
)
from src.ui.button import Button


TUTORIAL_STEPS = [
    {
        "title": "Welcome to 2048!",
        "text": [
            "Use arrow keys to slide all tiles",
            "in one direction.",
            "",
            "Tiles with the same number merge",
            "into one when they collide.",
        ],
    },
    {
        "title": "How to Move",
        "text": [
            "Press \u2190 \u2191 \u2192 \u2193 arrow keys or WASD",
            "to move tiles on the board.",
            "",
            "All tiles slide as far as possible",
            "in the chosen direction.",
        ],
    },
    {
        "title": "Merging Tiles",
        "text": [
            "When two tiles with the same value",
            "collide, they merge into one tile",
            "with double the value.",
            "",
            "Example: 2 + 2 = 4, 4 + 4 = 8",
        ],
    },
    {
        "title": "Scoring",
        "text": [
            "Your score increases by the value",
            "of each merged tile.",
            "",
            "Merging two 16s gives you 32 points.",
            "Try to reach the 2048 tile!",
        ],
    },
    {
        "title": "Tips",
        "text": [
            "Keep your highest tile in a corner.",
            "Build a chain of decreasing values.",
            "",
            "Press P to pause the game.",
            "Use Undo to fix mistakes (max 5).",
        ],
    },
]


class TutorialState(BaseState):
    """Step-by-step interactive tutorial."""

    def __init__(self, game):
        super().__init__(game)
        self.step = 0
        self.title_font = pygame.font.Font(None, 52)
        self.text_font = pygame.font.Font(None, 30)
        self.step_font = pygame.font.Font(None, 24)
        self.button_font = pygame.font.Font(None, 32)
        self.buttons = self._create_buttons()

    def _create_buttons(self) -> list[Button]:
        next_btn = Button(
            rect=pygame.Rect(WINDOW_WIDTH // 2 + 20, WINDOW_HEIGHT - 90, 120, 45),
            text="Next",
            font=self.button_font,
            color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text_color=BUTTON_TEXT_COLOR,
            callback=self._next_step,
        )
        skip_btn = Button(
            rect=pygame.Rect(WINDOW_WIDTH // 2 - 140, WINDOW_HEIGHT - 90, 120, 45),
            text="Skip",
            font=self.button_font,
            color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text_color=BUTTON_TEXT_COLOR,
            callback=lambda: self.game.change_state("menu"),
        )
        return [next_btn, skip_btn]

    def enter(self):
        self.step = 0

    def _next_step(self):
        self.step += 1
        if self.step >= len(TUTORIAL_STEPS):
            self.game.change_state("menu")

    def handle_event(self, event: pygame.event.Event):
        for button in self.buttons:
            button.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_state("menu")
            elif event.key in (pygame.K_RIGHT, pygame.K_RETURN, pygame.K_SPACE):
                self._next_step()

    def update(self, dt: float):
        pass

    def render(self, surface: pygame.Surface):
        surface.fill(BG_COLOR)

        if self.step >= len(TUTORIAL_STEPS):
            return

        step_data = TUTORIAL_STEPS[self.step]

        # Step indicator
        step_text = f"Step {self.step + 1} of {len(TUTORIAL_STEPS)}"
        step_surf = self.step_font.render(step_text, True, TITLE_COLOR)
        surface.blit(step_surf, (20, 20))

        # Title
        title_surf = self.title_font.render(step_data["title"], True, TITLE_COLOR)
        title_rect = title_surf.get_rect(centerx=WINDOW_WIDTH // 2, y=100)
        surface.blit(title_surf, title_rect)

        # Body text
        y = 220
        for line in step_data["text"]:
            if line:
                line_surf = self.text_font.render(line, True, TITLE_COLOR)
                line_rect = line_surf.get_rect(centerx=WINDOW_WIDTH // 2, y=y)
                surface.blit(line_surf, line_rect)
            y += 40

        # Demo board (simple visual)
        self._render_demo_board(surface)

        for button in self.buttons:
            button.render(surface)

    def _render_demo_board(self, surface: pygame.Surface):
        """Render a small illustrative 2x2 board."""
        cell_size = 60
        padding = 6
        start_x = (WINDOW_WIDTH - 2 * (cell_size + padding)) // 2
        start_y = 460
        demo_values = [[2, 4], [4, 2]]

        colors = {
            2: (238, 228, 218),
            4: (237, 224, 200),
        }
        text_color = (119, 110, 101)
        font = pygame.font.Font(None, 36)

        for r in range(2):
            for c in range(2):
                x = start_x + c * (cell_size + padding)
                y = start_y + r * (cell_size + padding)
                val = demo_values[r][c]
                color = colors.get(val, (205, 193, 180))
                pygame.draw.rect(surface, color, (x, y, cell_size, cell_size), border_radius=4)
                val_surf = font.render(str(val), True, text_color)
                val_rect = val_surf.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
                surface.blit(val_surf, val_rect)
