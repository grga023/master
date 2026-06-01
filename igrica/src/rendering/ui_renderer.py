"""UI elements rendering (score panel, buttons, header)."""

import pygame
from src.constants import (
    WINDOW_WIDTH, SCORE_BG_COLOR, SCORE_TEXT_COLOR, SCORE_LABEL_COLOR,
    TITLE_COLOR,
)


class UIRenderer:
    """Renders UI elements like score, title, and game info."""

    def __init__(self, theme_manager=None):
        self.theme_manager = theme_manager
        self._title_font = pygame.font.Font(None, 72)
        self._score_font = pygame.font.Font(None, 36)
        self._score_label_font = pygame.font.Font(None, 22)
        self._info_font = pygame.font.Font(None, 24)

    def render_header(self, surface: pygame.Surface, score: int, best_score: int):
        """Render the game header with title and scores."""
        title_color = self.theme_manager.get_color("title_color") if self.theme_manager else TITLE_COLOR
        title_surf = self._title_font.render("2048", True, title_color)
        surface.blit(title_surf, (30, 20))

        self._render_score_box(surface, WINDOW_WIDTH - 230, 20, 100, 55, "SCORE", score)
        self._render_score_box(surface, WINDOW_WIDTH - 120, 20, 100, 55, "BEST", best_score)

    def _render_score_box(self, surface: pygame.Surface, x: int, y: int,
                          width: int, height: int, label: str, value: int):
        """Render a score display box."""
        bg_color = self.theme_manager.get_color("score_bg") if self.theme_manager else SCORE_BG_COLOR

        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, bg_color, rect, border_radius=4)

        label_color = SCORE_LABEL_COLOR
        label_surf = self._score_label_font.render(label, True, label_color)
        label_rect = label_surf.get_rect(centerx=rect.centerx, top=rect.top + 5)
        surface.blit(label_surf, label_rect)

        text_color = SCORE_TEXT_COLOR
        value_surf = self._score_font.render(str(value), True, text_color)
        value_rect = value_surf.get_rect(centerx=rect.centerx, bottom=rect.bottom - 5)
        surface.blit(value_surf, value_rect)

    def render_subtitle(self, surface: pygame.Surface, text: str):
        """Render subtitle text below the title."""
        color = self.theme_manager.get_color("title_color") if self.theme_manager else TITLE_COLOR
        subtitle_surf = self._info_font.render(text, True, color)
        surface.blit(subtitle_surf, (30, 85))

    def render_game_info(self, surface: pygame.Surface, y: int, moves: int = 0,
                         undo_count: int = 0):
        """Render game info bar."""
        color = self.theme_manager.get_color("title_color") if self.theme_manager else TITLE_COLOR
        info_text = f"Moves: {moves}  |  Undos: {undo_count}/5"
        info_surf = self._info_font.render(info_text, True, color)
        surface.blit(info_surf, (30, y))
