"""Main gameplay state for 2048."""

import pygame

from src.states.base_state import BaseState
from src.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE,
    ANIMATION_SLIDE_DURATION, ANIMATION_MERGE_DURATION,
    ANIMATION_SPAWN_DURATION, PARTICLE_COUNT, PARTICLE_LIFETIME,
    BG_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR,
    SCORE_BG_COLOR, SCORE_TEXT_COLOR, SCORE_LABEL_COLOR, TITLE_COLOR,
)
from src.core.board import Board
from src.core.fibonacci_board import FibonacciBoard
from src.animation.animator import Animator
from src.animation.particles import ParticleSystem
from src.systems.input_handler import InputHandler
from src.ui.button import Button
from src.ui.toast import Toast, ToastManager
from src.educational.tips import get_tip_for_context, get_random_tip
from src.core.game_history import GameHistory
from src.ui.progress_tree import ProgressTree
from src.constants import TREE_PANEL_X, TREE_PANEL_WIDTH, MODE_FIBONACCI


MAX_UNDO = 5
EDUCATIONAL_TIP_INTERVAL = 30


class PlayState(BaseState):
    """Main gameplay: board movement, animations, scoring."""

    def __init__(self, game):
        super().__init__(game)
        self.board = Board(GRID_SIZE)
        self.animator = Animator()
        self.particles = ParticleSystem()
        self.input_handler = InputHandler()
        self.toast_manager = ToastManager()

        self.score = 0
        self.best_score = 0
        self.undo_stack: list[tuple] = []
        self.move_count = 0
        self.won = False
        self.animating = False
        self.history = GameHistory()
        self.progress_tree = ProgressTree(mode="classic")

        self.title_font = pygame.font.Font(None, 60)
        self.score_font = pygame.font.Font(None, 32)
        self.label_font = pygame.font.Font(None, 22)
        self.button_font = pygame.font.Font(None, 28)

        self._create_ui()

    def _create_ui(self):
        """Create score displays and action buttons."""
        self.undo_button = Button(
            rect=pygame.Rect(WINDOW_WIDTH - 130, 20, 55, 40),
            text="Undo",
            font=self.button_font,
            color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text_color=BUTTON_TEXT_COLOR,
            callback=self._undo,
        )
        self.hint_button = Button(
            rect=pygame.Rect(WINDOW_WIDTH - 65, 20, 55, 40),
            text="Hint",
            font=self.button_font,
            color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text_color=BUTTON_TEXT_COLOR,
            callback=self._show_hint,
        )

    def enter(self):
        """Start a new game or continue from save."""
        self.best_score = self.game.stats_manager.get_best_score()
        
        # Create board based on game mode
        game_mode = getattr(self.game, 'game_mode', 'classic')
        if game_mode == MODE_FIBONACCI:
            self.board = FibonacciBoard(GRID_SIZE)
        else:
            self.board = Board(GRID_SIZE)
        
        self.board.spawn_tile()
        self.board.spawn_tile()
        self.score = 0
        self.undo_stack = []
        self.move_count = 0
        self.won = False
        self.history.clear()
        self.progress_tree = ProgressTree(mode=game_mode)
        
        # Set tile colors for Fibonacci mode
        if game_mode == MODE_FIBONACCI:
            from src.constants import FIBONACCI_TILE_COLORS
            self.game.renderer.tile_renderer.color_override = FIBONACCI_TILE_COLORS
        else:
            self.game.renderer.tile_renderer.color_override = None

    def exit(self):
        """Save game state on exit."""
        save_data = {
            "grid": self.board.grid,
            "score": self.score,
            "move_count": self.move_count,
        }
        self.game.save_manager.save_game(save_data)
        # Store history for replay
        self.game.last_game_history = self.history

    def handle_event(self, event: pygame.event.Event):
        if self.animating:
            return

        self.undo_button.handle_event(event)
        self.hint_button.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                self.game.push_state("pause")
                return

        action = self.input_handler.process_event(event)
        if action and action.startswith("move_"):
            direction = action[5:]  # strip "move_" prefix
            self._execute_move(direction)

    def _execute_move(self, direction: str):
        """Process a move: save state, move board, animate, spawn."""
        if not self.board.can_move():
            return

        old_board = self.board.clone()
        old_score = self.score
        grid_before = [row[:] for row in self.board.grid]

        result = self.board.move(direction)
        if not result.board_changed:
            return

        # Save to undo stack
        self.undo_stack.append((old_board, old_score))
        if len(self.undo_stack) > MAX_UNDO:
            self.undo_stack.pop(0)

        self.score += result.score_gained
        if self.score > self.best_score:
            self.best_score = self.score
            self.game.stats_manager.set_best_score(self.best_score)

        self.move_count += 1

        # Record move in history
        self.history.record(grid_before, direction, old_score, self.score, self.move_count)

        # Create slide animations for each movement
        self.animating = True
        self.animator.clear()

        for i, movement in enumerate(result.movements):
            from src.rendering.grid_renderer import GridRenderer
            gr = self.game.renderer.grid_renderer
            sx, sy = gr.cell_to_pixel(movement.from_pos[0], movement.from_pos[1])
            ex, ey = gr.cell_to_pixel(movement.to_pos[0], movement.to_pos[1])
            self.animator.create_slide(f"{i}", sx, sy, ex, ey, ANIMATION_SLIDE_DURATION)

        # After all slides complete, handle merges and spawn
        self.animator.on_all_complete(lambda: self._on_slide_complete(result))

    def _on_slide_complete(self, result):
        """After slides finish, handle merges and spawn."""
        if result.merges:
            for i, merge in enumerate(result.merges):
                self.animator.create_merge(f"m{i}", ANIMATION_MERGE_DURATION)
                px = merge.pos[1] * 120 + 90
                py = merge.pos[0] * 120 + 240
                self.particles.emit(px, py, (255, 200, 100), PARTICLE_COUNT)
            self.game.audio_manager.play_sfx("merge")
            self.animator.on_all_complete(self._spawn_new_tile)
        else:
            self._spawn_new_tile()

    def _spawn_new_tile(self):
        """Spawn a new tile with animation, then check win/loss."""
        pos = self.board.spawn_tile()
        if pos:
            self.animator.create_spawn(f"s_{pos[0]}_{pos[1]}", ANIMATION_SPAWN_DURATION,
                                       on_complete=self._on_spawn_complete)
        else:
            self._on_spawn_complete()

    def _on_spawn_complete(self):
        """Check game state after spawn animation."""
        self.animating = False

        if self.board.has_won() and not self.won:
            self.won = True
            self.game.push_state("victory")
            return

        if not self.board.can_move():
            self.game.push_state("gameover")
            return

        # Periodic educational tip
        if self.move_count % EDUCATIONAL_TIP_INTERVAL == 0 and self.move_count > 0:
            tip = get_random_tip()
            self.toast_manager.show(tip, self.label_font)

    def _undo(self):
        """Restore previous board state."""
        if not self.undo_stack or self.animating:
            return
        board, score = self.undo_stack.pop()
        self.board = board
        self.score = score
        self.game.audio_manager.play_sfx("click")

    def _show_hint(self):
        """Display a contextual gameplay tip."""
        tip = get_tip_for_context(self.score, 0, self.move_count)
        self.toast_manager.show(tip, self.label_font)

    def update(self, dt: float):
        self.animator.update(dt)
        self.particles.update(dt)
        self.toast_manager.update(dt)
        self.progress_tree.update(dt, self.board.grid)

        if self.animating and not self.animator.is_animating:
            self.animating = False

    def render(self, surface: pygame.Surface):
        surface.fill(BG_COLOR)

        self._render_header(surface)
        self.game.renderer.render_game(
            surface, self.board.grid, self.score, self.best_score,
            self.animator, self.particles, self.move_count, len(self.undo_stack)
        )
        self.undo_button.render(surface)
        self.hint_button.render(surface)
        self.progress_tree.render(surface, TREE_PANEL_X, 180, TREE_PANEL_WIDTH, 500)
        self.toast_manager.render(surface, WINDOW_WIDTH, WINDOW_HEIGHT)

    def _render_header(self, surface: pygame.Surface):
        """Draw title and score boxes."""
        game_mode = getattr(self.game, 'game_mode', 'classic')
        title_text = "Fibonacci" if game_mode == MODE_FIBONACCI else "2048"
        title_surf = self.title_font.render(title_text, True, TITLE_COLOR)
        surface.blit(title_surf, (20, 20))

        # Score box
        self._render_score_box(surface, WINDOW_WIDTH - 260, 70, "SCORE", self.score)
        self._render_score_box(surface, WINDOW_WIDTH - 130, 70, "BEST", self.best_score)

    def _render_score_box(self, surface, x, y, label, value):
        """Render a score display box."""
        box_rect = pygame.Rect(x, y, 110, 55)
        pygame.draw.rect(surface, SCORE_BG_COLOR, box_rect, border_radius=4)

        label_surf = self.label_font.render(label, True, SCORE_LABEL_COLOR)
        label_rect = label_surf.get_rect(centerx=box_rect.centerx, y=y + 6)
        surface.blit(label_surf, label_rect)

        value_surf = self.score_font.render(str(value), True, SCORE_TEXT_COLOR)
        value_rect = value_surf.get_rect(centerx=box_rect.centerx, y=y + 26)
        surface.blit(value_surf, value_rect)
