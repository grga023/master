"""AI plays 2048 visually — watch the game unfold at a comfortable pace."""

import sys
import os
import time
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
from src.constants import *
from src.core.board import Board
from src.rendering.grid_renderer import GridRenderer
from src.rendering.tile_renderer import TileRenderer
from src.systems.theme_manager import ThemeManager


# --- AI Strategy (corner-based heuristic with 1-step lookahead) ---

def evaluate_board(grid, size=4):
    """Evaluate board position for AI decision-making."""
    score = 0.0
    max_val = 0
    empty = 0

    for r in range(size):
        for c in range(size):
            v = grid[r][c]
            if v == 0:
                empty += 1
            if v > max_val:
                max_val = v

    # More empty cells = better
    score += empty * 15

    # Max tile in bottom-left corner = big bonus
    if grid[size - 1][0] == max_val:
        score += max_val * 3
    elif max_val in (grid[0][0], grid[0][size-1], grid[size-1][size-1]):
        score += max_val * 1.5

    # Monotonicity along bottom row (descending left to right ideal)
    for c in range(size - 1):
        if grid[size-1][c] >= grid[size-1][c+1]:
            score += grid[size-1][c] * 0.5

    # Monotonicity along left column (descending bottom to top ideal)
    for r in range(size - 1):
        if grid[r+1][0] >= grid[r][0]:
            score += grid[r+1][0] * 0.5

    # Smoothness penalty (adjacent tiles with big difference)
    for r in range(size):
        for c in range(size):
            if grid[r][c] == 0:
                continue
            if c + 1 < size and grid[r][c+1] != 0:
                score -= abs(grid[r][c] - grid[r][c+1]) * 0.05
            if r + 1 < size and grid[r+1][c] != 0:
                score -= abs(grid[r][c] - grid[r+1][c]) * 0.05

    return score


def simulate_move(grid, direction, size=4):
    """Simulate a move and return (new_grid, score_gained)."""
    g = [row[:] for row in grid]

    if direction == "right":
        g = [r[::-1] for r in g]
    elif direction == "up":
        g = [[g[r][c] for r in range(size)] for c in range(size)]
    elif direction == "down":
        g = [[g[r][c] for r in range(size)] for c in range(size)]
        g = [r[::-1] for r in g]

    total_score = 0
    for i in range(size):
        nz = [x for x in g[i] if x != 0]
        merged = []
        skip = False
        for j in range(len(nz)):
            if skip:
                skip = False
                continue
            if j + 1 < len(nz) and nz[j] == nz[j + 1]:
                merged.append(nz[j] * 2)
                total_score += nz[j] * 2
                skip = True
            else:
                merged.append(nz[j])
        g[i] = merged + [0] * (size - len(merged))

    if direction == "right":
        g = [r[::-1] for r in g]
    elif direction == "up":
        g = [[g[c][r] for c in range(size)] for r in range(size)]
    elif direction == "down":
        g = [r[::-1] for r in g]
        g = [[g[c][r] for c in range(size)] for r in range(size)]

    return g, total_score


def ai_best_move(grid, size=4):
    """Pick the best move using 1-step lookahead with evaluation."""
    original = [row[:] for row in grid]
    best_score = float("-inf")
    best_dir = None

    # Prefer down/left to maintain corner strategy
    for d in ["down", "left", "right", "up"]:
        new_grid, score_gained = simulate_move(grid, d, size)
        if new_grid == original:
            continue
        val = evaluate_board(new_grid, size) + score_gained * 0.5
        if val > best_score:
            best_score = val
            best_dir = d

    return best_dir


# --- Visual Rendering ---

DIRECTION_ARROWS = {
    "left": "←",
    "right": "→",
    "up": "↑",
    "down": "↓",
}

def main():
    pygame.init()
    delay_per_move = 400  # milliseconds between moves (adjustable)

    # Window setup
    screen_w, screen_h = 650, 800
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("2048 AI Simulation — Watch me play!")
    clock = pygame.time.Clock()

    # Fonts
    title_font = pygame.font.Font(None, 52)
    score_font = pygame.font.Font(None, 38)
    info_font = pygame.font.Font(None, 28)
    tile_font_large = pygame.font.Font(None, 55)
    tile_font_medium = pygame.font.Font(None, 42)
    tile_font_small = pygame.font.Font(None, 34)

    # Board setup
    board = Board(4)
    board.spawn_tile()
    board.spawn_tile()

    score = 0
    moves = 0
    max_tile = 2
    last_direction = ""
    game_over = False
    paused = False

    # Grid rendering constants
    grid_x = 30
    grid_y = 180
    cell_size = 130
    cell_padding = 10
    grid_total = cell_size * 4 + cell_padding * 5

    # Tile color map
    tile_colors = {
        0: (205, 193, 180), 2: (238, 228, 218), 4: (237, 224, 200),
        8: (242, 177, 121), 16: (245, 149, 99), 32: (246, 124, 95),
        64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 204, 97),
        512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 46),
        4096: (60, 58, 50), 8192: (60, 58, 50),
    }

    move_timer = 0

    running = True
    while running:
        dt = clock.tick(60)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    delay_per_move = max(50, delay_per_move - 50)
                elif event.key == pygame.K_MINUS:
                    delay_per_move = min(2000, delay_per_move + 50)

        # AI makes a move
        if not game_over and not paused:
            move_timer += dt
            if move_timer >= delay_per_move:
                move_timer = 0
                direction = ai_best_move(board.grid, board.size)
                if direction:
                    result = board.move(direction)
                    if result.board_changed:
                        score += result.score_gained
                        board.spawn_tile()
                        moves += 1
                        last_direction = direction
                        # Update max tile
                        for row in board.grid:
                            for v in row:
                                if v > max_tile:
                                    max_tile = v
                        # Check game over
                        if not board.can_move():
                            game_over = True
                    else:
                        game_over = True
                else:
                    game_over = True

        # === RENDER ===
        screen.fill((250, 248, 239))

        # Title
        title_surf = title_font.render("2048 AI", True, (119, 110, 101))
        screen.blit(title_surf, (grid_x, 20))

        # Direction arrow
        if last_direction:
            arrow = DIRECTION_ARROWS.get(last_direction, "")
            arrow_surf = title_font.render(arrow, True, (143, 122, 102))
            screen.blit(arrow_surf, (grid_x + 180, 20))

        # Score & info
        score_surf = score_font.render(f"Score: {score}", True, (119, 110, 101))
        screen.blit(score_surf, (grid_x + 280, 20))

        moves_surf = info_font.render(f"Moves: {moves}  |  Max: {max_tile}", True, (143, 122, 102))
        screen.blit(moves_surf, (grid_x, 70))

        # Speed info
        speed_text = f"Speed: {delay_per_move}ms/move  [+/-]  |  Space: {'PAUSED' if paused else 'playing'}"
        speed_surf = info_font.render(speed_text, True, (160, 150, 140))
        screen.blit(speed_surf, (grid_x, 100))

        # Status
        if game_over:
            status_surf = score_font.render("GAME OVER!", True, (200, 50, 50))
            screen.blit(status_surf, (grid_x, 130))
        elif paused:
            status_surf = score_font.render("PAUSED", True, (50, 50, 200))
            screen.blit(status_surf, (grid_x, 130))

        # Grid background
        grid_bg_rect = pygame.Rect(grid_x, grid_y, grid_total, grid_total)
        pygame.draw.rect(screen, (187, 173, 160), grid_bg_rect, border_radius=8)

        # Draw tiles
        for r in range(4):
            for c in range(4):
                val = board.grid[r][c]
                x = grid_x + cell_padding + c * (cell_size + cell_padding)
                y = grid_y + cell_padding + r * (cell_size + cell_padding)

                # Cell background
                color = tile_colors.get(val, (60, 58, 50))
                cell_rect = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(screen, color, cell_rect, border_radius=6)

                # Number text
                if val != 0:
                    text = str(val)
                    if len(text) <= 2:
                        font = tile_font_large
                    elif len(text) == 3:
                        font = tile_font_medium
                    else:
                        font = tile_font_small

                    text_color = (119, 110, 101) if val <= 4 else (249, 246, 242)
                    text_surf = font.render(text, True, text_color)
                    text_rect = text_surf.get_rect(center=cell_rect.center)
                    screen.blit(text_surf, text_rect)

        # Bottom info: last few moves
        hint_surf = info_font.render("ESC to quit  |  Space to pause  |  +/- to change speed", True, (160, 150, 140))
        screen.blit(hint_surf, (grid_x, grid_y + grid_total + 20))

        pygame.display.flip()

    pygame.quit()
    print(f"\nGame ended! Score: {score}, Moves: {moves}, Max tile: {max_tile}")


if __name__ == "__main__":
    main()
