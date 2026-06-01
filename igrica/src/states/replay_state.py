"""Strategy replay state for reviewing game history."""
import pygame

from src.states.base_state import BaseState
from src.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y,
    CELL_SIZE, CELL_PADDING, BG_COLOR,
    BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR, TITLE_COLOR,
)
from src.ui.button import Button
from src.ui.timeline_bar import TimelineBar


class ReplayState(BaseState):
    """Replay recorded game history with playback controls."""

    SPEEDS = [1.0, 2.0, 5.0]
    SPEED_LABELS = ["1x", "2x", "5x"]
    AUTO_STEP_INTERVAL = 800  # ms at 1x speed

    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.Font(None, 48)
        self.info_font = pygame.font.Font(None, 32)
        self.button_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 24)

        self.entries = []
        self.current_idx = 0
        self.playing = False
        self.speed_idx = 0
        self.elapsed = 0.0
        self.timeline = None
        self.buttons = []

    def enter(self):
        """Load history from game object."""
        history = getattr(self.game, 'last_game_history', None)
        if history and history.total_moves > 0:
            self.entries = history.get_entries()
            milestones = [i for i, e in enumerate(self.entries) if e.is_milestone]
            self.timeline = TimelineBar(
                rect=pygame.Rect(30, WINDOW_HEIGHT - 60, WINDOW_WIDTH - 60, 20),
                total_steps=len(self.entries) - 1,
                milestones=milestones,
            )
        else:
            self.entries = []
            self.timeline = None

        self.current_idx = 0
        self.playing = False
        self.speed_idx = 0
        self.elapsed = 0.0
        self._create_buttons()

    def _create_buttons(self):
        """Create playback control buttons."""
        self.buttons = []
        btn_y = WINDOW_HEIGHT - 110
        btn_h = 36
        btn_w = 80
        spacing = 10
        start_x = 30

        # Step back
        self.buttons.append(Button(
            rect=pygame.Rect(start_x, btn_y, 50, btn_h),
            text="◀◀", font=self.button_font,
            color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR,
            text_color=BUTTON_TEXT_COLOR,
            callback=self._step_back,
        ))
        # Play/Pause
        self.buttons.append(Button(
            rect=pygame.Rect(start_x + 60, btn_y, 70, btn_h),
            text="Play", font=self.button_font,
            color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR,
            text_color=BUTTON_TEXT_COLOR,
            callback=self._toggle_play,
        ))
        # Step forward
        self.buttons.append(Button(
            rect=pygame.Rect(start_x + 140, btn_y, 50, btn_h),
            text="▶▶", font=self.button_font,
            color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR,
            text_color=BUTTON_TEXT_COLOR,
            callback=self._step_forward,
        ))
        # Speed
        self.buttons.append(Button(
            rect=pygame.Rect(start_x + 200, btn_y, 60, btn_h),
            text="1x", font=self.button_font,
            color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR,
            text_color=BUTTON_TEXT_COLOR,
            callback=self._cycle_speed,
        ))
        # Back to menu
        self.buttons.append(Button(
            rect=pygame.Rect(WINDOW_WIDTH - 150, btn_y, 120, btn_h),
            text="Back", font=self.button_font,
            color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR,
            text_color=BUTTON_TEXT_COLOR,
            callback=lambda: self.game.change_state("menu"),
        ))

    def _toggle_play(self):
        self.playing = not self.playing
        self.buttons[1].text = "Pause" if self.playing else "Play"

    def _step_forward(self):
        if self.current_idx < len(self.entries) - 1:
            self.current_idx += 1
            self._sync_timeline()

    def _step_back(self):
        if self.current_idx > 0:
            self.current_idx -= 1
            self._sync_timeline()

    def _cycle_speed(self):
        self.speed_idx = (self.speed_idx + 1) % len(self.SPEEDS)
        self.buttons[3].text = self.SPEED_LABELS[self.speed_idx]

    def _sync_timeline(self):
        if self.timeline:
            self.timeline.set_step(self.current_idx)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_state("menu")
                return
            elif event.key == pygame.K_SPACE:
                self._toggle_play()
                return
            elif event.key == pygame.K_RIGHT:
                self._step_forward()
                return
            elif event.key == pygame.K_LEFT:
                self._step_back()
                return

        for button in self.buttons:
            button.handle_event(event)

        # Timeline click
        if event.type == pygame.MOUSEBUTTONDOWN and self.timeline:
            step = self.timeline.get_clicked_step(event.pos)
            if step is not None:
                self.current_idx = min(step, len(self.entries) - 1)
                self._sync_timeline()

    def update(self, dt: float):
        if not self.entries:
            return

        if self.playing:
            speed = self.SPEEDS[self.speed_idx]
            self.elapsed += dt
            interval = self.AUTO_STEP_INTERVAL / speed
            if self.elapsed >= interval:
                self.elapsed = 0.0
                if self.current_idx < len(self.entries) - 1:
                    self.current_idx += 1
                    self._sync_timeline()
                else:
                    self.playing = False
                    self.buttons[1].text = "Play"

    def render(self, surface: pygame.Surface):
        surface.fill(BG_COLOR)

        if not self.entries:
            msg = self.title_font.render("No replay data", True, TITLE_COLOR)
            surface.blit(msg, msg.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)))
            for btn in self.buttons:
                btn.render(surface)
            return

        entry = self.entries[self.current_idx]

        # Header info
        title_surf = self.title_font.render("Strategy Replay", True, TITLE_COLOR)
        surface.blit(title_surf, (20, 15))

        move_text = f"Move {entry.move_num}  |  Score: {entry.score_before}  |  Dir: {entry.direction}"
        info_surf = self.info_font.render(move_text, True, TITLE_COLOR)
        surface.blit(info_surf, (20, 60))

        # Determine border color for move quality
        border_color = None
        if entry.score_after > entry.score_before:
            border_color = (100, 200, 100)  # green: score increased
        elif self.current_idx > 0:
            prev_entry = self.entries[self.current_idx - 1]
            prev_empty = sum(1 for row in prev_entry.grid for v in row if v == 0)
            curr_empty = sum(1 for row in entry.grid for v in row if v == 0)
            if curr_empty < prev_empty - 2:
                border_color = (220, 80, 80)  # red: lost many empty cells

        # Render grid with border
        grid_x = GRID_OFFSET_X - CELL_PADDING
        grid_y = GRID_OFFSET_Y - CELL_PADDING
        grid_w = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * CELL_PADDING
        grid_h = grid_w

        if border_color:
            border_rect = pygame.Rect(grid_x - 4, grid_y - 4, grid_w + 8, grid_h + 8)
            pygame.draw.rect(surface, border_color, border_rect, width=4, border_radius=10)

        # Draw grid background
        grid_rect = pygame.Rect(grid_x, grid_y, grid_w, grid_h)
        pygame.draw.rect(surface, (187, 173, 160), grid_rect, border_radius=8)

        # Draw tiles
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = GRID_OFFSET_X + col * (CELL_SIZE + CELL_PADDING)
                y = GRID_OFFSET_Y + row * (CELL_SIZE + CELL_PADDING)
                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surface, (205, 193, 180), cell_rect, border_radius=6)

                value = entry.grid[row][col]
                if value != 0:
                    self.game.renderer.tile_renderer.render_tile(surface, x, y, value)

        # Progress text
        progress = f"{self.current_idx + 1} / {len(self.entries)}"
        prog_surf = self.small_font.render(progress, True, TITLE_COLOR)
        surface.blit(prog_surf, (WINDOW_WIDTH - 100, 20))

        # Max tile indicator
        max_text = f"Max tile: {entry.max_tile}"
        max_surf = self.small_font.render(max_text, True, TITLE_COLOR)
        surface.blit(max_surf, (WINDOW_WIDTH - 150, 45))

        # Timeline
        if self.timeline:
            self.timeline.render(surface)

        # Buttons
        for btn in self.buttons:
            btn.render(surface)
