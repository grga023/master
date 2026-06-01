"""Main renderer orchestrator that coordinates all rendering subsystems."""

import pygame
from typing import Optional
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, GRID_OFFSET_X, GRID_OFFSET_Y, CELL_SIZE, CELL_PADDING
from src.rendering.grid_renderer import GridRenderer
from src.rendering.tile_renderer import TileRenderer
from src.rendering.ui_renderer import UIRenderer
from src.animation.animator import Animator
from src.animation.particles import ParticleSystem
from src.systems.theme_manager import ThemeManager


class Renderer:
    """Main rendering orchestrator for the 2048 game."""

    def __init__(self, theme_manager: Optional[ThemeManager] = None):
        self.theme_manager = theme_manager or ThemeManager()
        self.grid_renderer = GridRenderer(self.theme_manager)
        self.tile_renderer = TileRenderer(self.theme_manager)
        self.ui_renderer = UIRenderer(self.theme_manager)

    def get_bg_color(self) -> tuple:
        """Get current background color from theme."""
        return self.theme_manager.get_color("bg_color")

    def render_game(self, surface: pygame.Surface, grid: list[list[int]],
                    score: int, best_score: int, animator: Optional[Animator] = None,
                    particles: Optional[ParticleSystem] = None,
                    moves: int = 0, undo_count: int = 0):
        """Render the complete game screen."""
        surface.fill(self.get_bg_color())

        self.ui_renderer.render_header(surface, score, best_score)
        self.ui_renderer.render_subtitle(surface, "Join the numbers and get to the 2048 tile!")
        self.ui_renderer.render_game_info(surface, 110, moves, undo_count)

        self.grid_renderer.render(surface)

        self._render_tiles(surface, grid, animator)

        if particles:
            particles.render(surface)

    def _render_tiles(self, surface: pygame.Surface, grid: list[list[int]],
                      animator: Optional[Animator] = None):
        """Render all tiles with animation support."""
        size = len(grid)
        for row in range(size):
            for col in range(size):
                value = grid[row][col]
                if value == 0:
                    continue

                x, y = self.grid_renderer.cell_to_pixel(row, col)

                scale = 1.0
                alpha = 255
                tile_id = f"{row}_{col}"

                if animator:
                    spawn_anim = animator.get_animation(f"spawn_{tile_id}")
                    if spawn_anim and not spawn_anim.completed:
                        scale = spawn_anim.get_value("scale")
                        alpha = int(spawn_anim.get_value("alpha"))

                    merge_anim = animator.get_animation(f"merge_{tile_id}")
                    if merge_anim and not merge_anim.completed:
                        scale = merge_anim.get_value("scale")

                self.tile_renderer.render_tile(surface, x, y, value, scale, alpha)

    def render_overlay(self, surface: pygame.Surface, text: str,
                       sub_text: str = "", alpha: int = 180):
        """Render a semi-transparent overlay with text."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        surface.blit(overlay, (0, 0))

        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)

        text_surf = font_large.render(text, True, (249, 246, 242))
        text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        surface.blit(text_surf, text_rect)

        if sub_text:
            sub_surf = font_small.render(sub_text, True, (220, 220, 220))
            sub_rect = sub_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
            surface.blit(sub_surf, sub_rect)
