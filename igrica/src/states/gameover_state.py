"""Game over overlay state."""

import pygame

from src.states.base_state import BaseState
from src.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR,
)
from src.ui.button import Button


class GameOverState(BaseState):
    """Game over screen with final score and retry options."""

    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.Font(None, 72)
        self.score_font = pygame.font.Font(None, 42)
        self.button_font = pygame.font.Font(None, 36)
        self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))
        self.final_score = 0
        self.buttons = self._create_buttons()

    def _create_buttons(self) -> list[Button]:
        button_width = 200
        button_height = 50
        spacing = 20
        start_y = WINDOW_HEIGHT // 2 + 40

        items = [
            ("Try Again", lambda: self.game.change_state("play")),
            ("Watch Replay", lambda: self.game.change_state("replay")),
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
        """Save high score on game over."""
        play_state = self.game.states.get("play")
        self.final_score = play_state.score if play_state else 0
        best = self.game.stats_manager.get_best_score()
        if self.final_score > best:
            self.game.stats_manager.set_best_score(self.final_score)
        self.game.audio_manager.play_sfx("gameover")
        # Show/hide replay button based on history availability
        has_history = (hasattr(self.game, 'last_game_history') and
                      self.game.last_game_history and
                      self.game.last_game_history.total_moves > 0)
        if len(self.buttons) > 1:
            self.buttons[1].visible = has_history
            self.buttons[1].enabled = has_history

    def handle_event(self, event: pygame.event.Event):
        for button in self.buttons:
            button.handle_event(event)

    def update(self, dt: float):
        pass

    def render(self, surface: pygame.Surface):
        surface.blit(self.overlay, (0, 0))

        title_surf = self.title_font.render("Game Over!", True, (255, 255, 255))
        title_rect = title_surf.get_rect(centerx=WINDOW_WIDTH // 2, y=WINDOW_HEIGHT // 2 - 100)
        surface.blit(title_surf, title_rect)

        score_text = f"Score: {self.final_score}"
        score_surf = self.score_font.render(score_text, True, (255, 255, 255))
        score_rect = score_surf.get_rect(centerx=WINDOW_WIDTH // 2, y=WINDOW_HEIGHT // 2 - 20)
        surface.blit(score_surf, score_rect)

        for button in self.buttons:
            button.render(surface)
